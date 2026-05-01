import sys
from pathlib import Path

# Ensure the repository root is on sys.path when running this script directly.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agentic_engine import AgenticRecommender
from src.recommender import load_songs


def run_evaluation():
    songs = load_songs("data/songs.csv")
    engine = AgenticRecommender(songs)

    scenarios = [
        {
            "name": "Stressed and needs focus",
            "input": "I'm stressed and need to focus on my work",
        },
        {
            "name": "Happy workout session",
            "input": "I want an upbeat high-energy playlist for the gym",
        },
        {
            "name": "Relaxing evening",
            "input": "Something calm and chill for winding down after a long day",
        },
        {
            "name": "Concentration study music",
            "input": "Play something focused and low-distraction for studying",
        },
        {
            "name": "Dance party mix",
            "input": "Give me a happy dance playlist with strong tempo",
        },
    ]

    total_confidence = 0.0
    passed_count = 0

    print("Agentic Evaluation Harness")
    print("=" * 30)

    for scenario in scenarios:
        recommendations = engine.recommend(scenario["input"], k=5)
        top_confidence = recommendations[0].confidence if recommendations else 0.0
        total_confidence += top_confidence
        passed = top_confidence >= 0.7
        if passed:
            passed_count += 1

        print(f"Scenario: {scenario['name']}")
        print(f"User Input: {scenario['input']}")
        print(f"Top Recommendation Confidence: {top_confidence:.2f}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")

        for rank, rec in enumerate(recommendations[:3], start=1):
            print(f"  {rank}. {rec.song['title']} by {rec.song['artist']} (confidence={rec.confidence:.2f})")
        print("-" * 30)

    average_confidence = total_confidence / len(scenarios)
    print("Evaluation Summary")
    print(f"Passed {passed_count}/{len(scenarios)} scenarios")
    print(f"Average top confidence: {average_confidence:.2f}")


if __name__ == "__main__":
    run_evaluation()
