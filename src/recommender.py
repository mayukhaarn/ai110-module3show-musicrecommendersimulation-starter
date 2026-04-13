import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries.
    
    Args:
        csv_path (str): Path to the CSV file (e.g., 'data/songs.csv').
    
    Returns:
        List[Dict]: A list of dictionaries, each representing a song with keys:
                    id, title, artist, genre, mood, energy, tempo_bpm,
                    valence, danceability, acousticness.
    
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If a row is missing required columns or type conversion fails.
    """
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate that the header exists
            if reader.fieldnames is None:
                raise ValueError(f"CSV file {csv_path} appears to be empty or malformed.")
            
            for row_num, row in enumerate(reader, start=2):  # start=2 because header is row 1
                try:
                    # Type conversion: numerical columns to float/int
                    song = {
                        'id': int(row['id']),
                        'title': row['title'],
                        'artist': row['artist'],
                        'genre': row['genre'],
                        'mood': row['mood'],
                        'energy': float(row['energy']),
                        'tempo_bpm': int(row['tempo_bpm']),
                        'valence': float(row['valence']),
                        'danceability': float(row['danceability']),
                        'acousticness': float(row['acousticness']),
                    }
                    songs.append(song)
                
                except (KeyError, ValueError) as e:
                    print(f"Warning: Skipping row {row_num} due to type conversion error: {e}")
                    continue
        
        print(f"Successfully loaded {len(songs)} songs from {csv_path}.")
        return songs
    
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at {csv_path}.")
    except Exception as e:
        raise Exception(f"Unexpected error loading CSV from {csv_path}: {e}")

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
