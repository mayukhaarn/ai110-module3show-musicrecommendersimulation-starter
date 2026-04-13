"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, get_recommendations


def main() -> None:
    # Data Loading
    all_songs = load_songs("data/songs.csv")

    # Profile Definition
    taste_profile = {
        "favorite_genre": "Pop",
        "favorite_mood": "happy", 
        "target_energy": 0.8
    }

    # Processing
    recommendations = get_recommendations(taste_profile, all_songs, k=3)

    # Formatted Output
    print("\nTop 3 Song Recommendations:\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"     - {reason}")
        print()

    # Final Touch
    print("Recommendation process complete!")


if __name__ == "__main__":
    main()
