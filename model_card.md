# 🎧 Model Card: Agentic Music Recommender

## 1. Model Name

**Agentic VibeFinder** — a compact music recommendation engine that uses a planning agent, a retrieval tool, and a critic to deliver playlist suggestions with confidence scoring.

## 2. Intended Use

This system is designed for educational exploration and prototype evaluation, not for production deployment. It is meant to demonstrate how an agentic recommendation pipeline can interpret user mood descriptions and validate music choices with explicit confidence.

## 3. How It Works

The system works in three stages:

- A **Planner Agent** parses user input and maps it to search parameters like energy, valence, tempo, mood, and optional genre.
- A **Retrieval Tool** uses the existing recommendation engine to build a candidate pool from the song catalog and ranks candidates with the inferred search parameters.
- A **Critic Agent** validates the resulting songs, rejects options that are out of alignment with the user's intent, and computes a normalized confidence score for each recommendation.

The pipeline follows a `Plan -> Act -> Reflect` loop, which makes the recommendation process easier to inspect and explain.

## 4. Data

The model uses the dataset in `data/songs.csv`.

- **Catalog size:** 11 songs
- **Genres included:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, disco
- **Moods included:** happy, chill, intense, relaxed, moody, focused
- **Energy range:** 0.28 to 0.93

This dataset is intentionally small and biased toward Western pop and lofi styles. It is sufficient for classroom exploration but not for broad music discovery.

## 5. Strengths

- **Modular reasoning:** Planner, retriever, and critic are separated into distinct components.
- **Transparency:** Each recommendation includes explicit reasoning and a confidence score.
- **Reliability harness:** A simple end-to-end test script verifies candidate confidence across scenarios.
- **Refinement support:** The system attempts to relax constraints if the critic rejects all initial candidates.

## 6. Limitations and Bias

**Genre bias:** The dataset over-represents pop and lofi, which means recommendations are more reliable for those styles and less reliable for genres that are missing.

**Mood coverage bias:** Moods like "sad" are underrepresented, so requests for those moods may degrade to energy-based matches rather than true emotional alignment.

**Temporally limited dataset:** Only 11 songs are available, so the system cannot model real-world recommendation diversity or serendipity.

**Potential misuse:** The model could be misinterpreted as a full music recommendation service. In a production context, that could lead to addictive feedback loops if users are shown only high-confidence but narrow playlists.

## 7. Evaluation

Evaluation is performed using `tests/eval_harness.py`, which:

- runs five predefined user scenarios
- prints pass/fail results using a 0.7 confidence threshold
- computes average top recommendation confidence

This provides a reproducible reliability check for the agentic workflow.

## 8. Potential Misuse

This prototype is not intended for live deployment. Misuse risks include:

- presenting biased recommendations as if they were comprehensive
- reinforcing mood stereotypes by mapping language to fixed energy/genre choices
- generating narrow playlists that encourage repetitive listening patterns

## 9. AI Collaboration

GitHub Copilot helped accelerate the code scaffolding and structure for the planner/retriever/critic pipeline. Copilot's suggestions were useful for the logging pattern and for the general agentic design, but I had to correct several details to fit the dataset and avoid over-generalization.

A specific correction was needed for the planner logic: Copilot initially suggested a generic LLM-style mapping of mood text, but I adjusted it to use the actual dataset genres and moods present in `data/songs.csv`.

This collaboration shows where the AI can speed up engineering and where human judgment is still required to align design with real data.
