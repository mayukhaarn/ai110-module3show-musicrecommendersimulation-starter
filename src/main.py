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

    # Test Profiles
    profiles = [
        {
            "name": "Conflicting Data: High-Energy Sad Music",
            "prefs": {
                "favorite_genre": "Pop",
                "favorite_mood": "sad",  # No songs have "sad" mood
                "target_energy": 0.9
            }
        },
        {
            "name": "Empty/Rare Data: Classical Music Lover", 
            "prefs": {
                "favorite_genre": "classical",  # No songs have "classical" genre
                "favorite_mood": "relaxed",
                "target_energy": 0.3
            }
        },
        {
            "name": "Boundary Testing: Extreme Low Energy Seeker",
            "prefs": {
                "favorite_genre": "ambient",
                "favorite_mood": "chill", 
                "target_energy": 0.0  # Outside dataset range (0.28-0.93)
            }
        }
    ]

    for profile in profiles:
        print(f"\n{'='*60}")
        print(f"TESTING: {profile['name']}")
        print(f"Profile: {profile['prefs']}")
        print(f"{'='*60}")

        # Processing
        recommendations = get_recommendations(profile['prefs'], all_songs, k=3)

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
    print("All adversarial profile tests complete!")


if __name__ == "__main__":
    main()
