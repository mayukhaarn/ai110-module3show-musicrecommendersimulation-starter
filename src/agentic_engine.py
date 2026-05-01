import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

from src.recommender import get_recommendations

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("assets/agentic_engine.log", mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logger.addHandler(file_handler)


@dataclass
class Recommendation:
    song: Dict
    score: float
    confidence: float
    reasons: List[str]
    plan: Dict


class PlannerAgent:
    """Convert human mood language into structured recommendation parameters."""

    def parse_intent(self, user_input: str) -> Dict:
        text = user_input.lower()
        plan = {
            "intent": user_input,
            "favorite_genre": "",
            "favorite_mood": "",
            "target_energy": 0.55,
            "target_valence": 0.55,
            "target_tempo": 0.55,
            "notes": [],
        }

        if "stressed" in text or "anxious" in text or "overwhelmed" in text:
            plan["favorite_mood"] = "relaxed"
            plan["target_energy"] = 0.35
            plan["target_valence"] = 0.45
            plan["target_tempo"] = 0.30
            plan["notes"].append("inferred calm, low-energy mood from stress")

        if "focus" in text or "focused" in text or "study" in text or "work" in text:
            plan["favorite_mood"] = "focused"
            plan["target_energy"] = max(plan["target_energy"], 0.50)
            plan["target_valence"] = 0.55
            plan["target_tempo"] = 0.45
            plan["notes"].append("inferred focused listening mode")

        if "workout" in text or "gym" in text or "run" in text or "training" in text:
            plan["favorite_mood"] = "intense"
            plan["target_energy"] = 0.90
            plan["target_valence"] = 0.70
            plan["target_tempo"] = 0.85
            plan["notes"].append("inferred high-energy workout intent")

        if "relax" in text or "sleep" in text or "wind down" in text:
            plan["favorite_mood"] = plan.get("favorite_mood", "relaxed") or "relaxed"
            plan["target_energy"] = 0.30
            plan["target_valence"] = 0.45
            plan["target_tempo"] = 0.25
            plan["notes"].append("inferred relaxation intent")

        if "happy" in text or "uplifting" in text or "positive" in text or "party" in text:
            plan["favorite_mood"] = "happy"
            plan["target_valence"] = 0.80
            plan["target_energy"] = max(plan["target_energy"], 0.65)
            plan["target_tempo"] = max(plan["target_tempo"], 0.65)
            plan["notes"].append("inferred upbeat mood")

        if "sad" in text or "moody" in text or "melancholy" in text:
            plan["favorite_mood"] = "moody"
            plan["target_valence"] = 0.30
            plan["target_energy"] = min(plan["target_energy"], 0.45)
            plan["target_tempo"] = min(plan["target_tempo"], 0.45)
            plan["notes"].append("inferred lower valence mood")

        if "chill" in text or "calm" in text or "easy" in text or "ambient" in text:
            plan["favorite_mood"] = "chill"
            plan["target_energy"] = 0.40
            plan["target_valence"] = 0.55
            plan["target_tempo"] = 0.35
            plan["notes"].append("inferred chill mood")

        if "indie" in text or "disco" in text or "jazz" in text or "lofi" in text or "pop" in text or "rock" in text or "ambient" in text or "synthwave" in text:
            for genre in ["indie pop", "disco", "jazz", "lofi", "pop", "rock", "ambient", "synthwave"]:
                if genre in text:
                    plan["favorite_genre"] = genre
                    plan["notes"].append(f"inferred genre preference: {genre}")
                    break

        if "focus" in text and not plan["favorite_mood"]:
            plan["favorite_mood"] = "focused"
            plan["notes"].append("fallback focused mood")

        if not plan["favorite_mood"] and "relaxed" in text:
            plan["favorite_mood"] = "relaxed"

        if not plan["favorite_genre"] and "jazz" in text:
            plan["favorite_genre"] = "jazz"

        logger.debug("Planner output: %s", plan)
        return plan


class RetrievalTool:
    """Fetch a candidate pool using the existing recommendation logic."""

    def __init__(self, songs: List[Dict]):
        self.songs = songs

    def retrieve(self, plan: Dict, k: int = 10) -> List[Tuple[Dict, float, List[str]]]:
        user_prefs = {
            "favorite_genre": plan["favorite_genre"],
            "favorite_mood": plan["favorite_mood"],
            "target_energy": plan["target_energy"],
        }
        raw_pool = get_recommendations(user_prefs, self.songs, k=max(k * 2, 10))

        enhanced_pool = []
        for song, score, reasons in raw_pool:
            tempo_norm = min(1.0, song.get("tempo_bpm", 120) / 200.0)
            tempo_score = 1.0 - abs(tempo_norm - plan["target_tempo"])
            valence_score = 1.0 - abs(song.get("valence", 0.5) - plan["target_valence"])
            bonus = max(0.0, tempo_score * 0.15) + max(0.0, valence_score * 0.15)
            enhanced_score = score + bonus
            enhanced_reasons = reasons + [f"Tempo match ({tempo_score:.2f})", f"Valence match ({valence_score:.2f})"]
            enhanced_pool.append((song, enhanced_score, enhanced_reasons))

        enhanced_pool.sort(key=lambda item: item[1], reverse=True)
        final_pool = enhanced_pool[:k]
        logger.debug("Retrieval result pool size=%d", len(final_pool))
        return final_pool


class CriticAgent:
    """Evaluate candidate songs against the user's mood and energy intent."""

    def calculate_confidence(self, song: Dict, score: float, plan: Dict) -> float:
        energy_fit = max(0.0, 1.0 - abs(song.get("energy", 0.5) - plan["target_energy"]))
        valence_fit = max(0.0, 1.0 - abs(song.get("valence", 0.5) - plan["target_valence"]))
        tempo_norm = min(1.0, song.get("tempo_bpm", 120) / 200.0)
        tempo_fit = max(0.0, 1.0 - abs(tempo_norm - plan["target_tempo"]))
        genre_fit = 1.0 if plan["favorite_genre"] and song.get("genre", "").lower() == plan["favorite_genre"].lower() else 0.5
        mood_fit = 1.0 if plan["favorite_mood"] and song.get("mood", "").lower() == plan["favorite_mood"].lower() else 0.5

        confidence = (energy_fit * 2.0 + valence_fit + tempo_fit + genre_fit + mood_fit) / 6.0
        confidence = max(0.0, min(1.0, confidence))
        return round(confidence, 2)

    def evaluate(self, plan: Dict, pool: List[Tuple[Dict, float, List[str]]], k: int = 5) -> Tuple[List[Recommendation], bool]:
        final_recommendations: List[Recommendation] = []
        rejected = []

        for song, score, reasons in pool:
            confidence = self.calculate_confidence(song, score, plan)
            mismatch_reason = self._detect_energy_mismatch(song, plan)
            reason_list = list(reasons)

            if mismatch_reason:
                reason_list.append(mismatch_reason)
                rejected.append((song, score, reason_list))
                continue

            reason_list.append(f"Confidence estimate: {confidence:.2f}")
            final_recommendations.append(Recommendation(song, score, confidence, reason_list, plan))

        if not final_recommendations:
            logger.warning("Critic rejected all candidates. Plan requires refinement.")
            for song, score, reasons in rejected:
                logger.debug("Rejected song=%s reasons=%s", song.get("title"), reasons)
            return [], True

        return final_recommendations[:k], False

    def _detect_energy_mismatch(self, song: Dict, plan: Dict) -> str:
        energy = song.get("energy", 0.5)
        if plan["target_energy"] <= 0.4 and energy > 0.75:
            return "Rejected by critic: too high energy for a calm/stressed listener"
        if plan["target_energy"] >= 0.8 and energy < 0.45:
            return "Rejected by critic: too low energy for an active/high-energy listener"
        return ""


class AgenticRecommender:
    """Orchestrates planning, retrieval, and critique as a reasoning loop."""

    def __init__(self, songs: List[Dict]):
        self.planner = PlannerAgent()
        self.retriever = RetrievalTool(songs)
        self.critic = CriticAgent()

    def recommend(self, user_input: str, k: int = 5) -> List[Recommendation]:
        try:
            plan = self.planner.parse_intent(user_input)
            pool = self.retriever.retrieve(plan, k=k * 2)
            recommendations, needs_refinement = self.critic.evaluate(plan, pool, k=k)

            if needs_refinement:
                plan = self._refine_plan(plan)
                pool = self.retriever.retrieve(plan, k=k * 2)
                recommendations, _ = self.critic.evaluate(plan, pool, k=k)

            if not recommendations:
                logger.info("Falling back to raw retrieval results without strict critic filtering.")
                recommendations = [
                    Recommendation(song, score, self.critic.calculate_confidence(song, score, plan), reasons, plan)
                    for song, score, reasons in pool[:k]
                ]

            logger.info("Generated %d recommendations for input: %s", len(recommendations), user_input)
            return recommendations

        except Exception as exc:
            logger.exception("Reasoning loop failure for input: %s", user_input)
            return []

    def _refine_plan(self, plan: Dict) -> Dict:
        plan = dict(plan)
        if plan["favorite_genre"]:
            plan["favorite_genre"] = ""
            plan["notes"].append("dropped genre constraint to improve result coverage")

        if plan["favorite_mood"] in {"relaxed", "focused"}:
            plan["target_energy"] = min(0.55, max(0.35, plan["target_energy"]))
            plan["target_tempo"] = min(0.55, max(0.35, plan["target_tempo"]))
            plan["notes"].append("softened energy and tempo targets during refinement")

        logger.debug("Refined plan: %s", plan)
        return plan
