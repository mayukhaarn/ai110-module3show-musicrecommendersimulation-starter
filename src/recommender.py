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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Calculate a match score for a song based on user preferences.
    
    Algorithm Recipe:
    - Genre Match: +2.0 points if song['genre'] == user_prefs['favorite_genre']
    - Mood Match: +1.0 point if song['mood'] == user_prefs['favorite_mood']
    - Energy Similarity: 1 - |song['energy'] - user_prefs['target_energy']| (0.0 to 1.0)
    
    Args:
        user_prefs (Dict): User preference profile with keys:
                          'favorite_genre', 'favorite_mood', 'target_energy'
        song (Dict): Song dictionary with keys:
                    'genre', 'mood', 'energy', etc.
    
    Returns:
        Tuple[float, List[str]]: A tuple containing:
                                 - score (float): Total composite score (max ~4.0)
                                 - reasons (List[str]): List of justifications for points awarded
    """
    score = 0.0
    reasons = []
    
    # Genre Match: +2.0 points
    try:
        if song.get('genre', '').lower() == user_prefs.get('favorite_genre', '').lower():
            score += 2.0
            reasons.append("Genre match (+2.0)")
    except (KeyError, AttributeError, TypeError):
        pass  # Gracefully handle missing or invalid genre data
    
    # Mood Match: +1.0 point
    try:
        if song.get('mood', '').lower() == user_prefs.get('favorite_mood', '').lower():
            score += 1.0
            reasons.append("Mood match (+1.0)")
    except (KeyError, AttributeError, TypeError):
        pass  # Gracefully handle missing or invalid mood data
    
    # Energy Similarity: 0.0 to 1.0 based on proximity
    try:
        song_energy = float(song.get('energy', 0.0))
        target_energy = float(user_prefs.get('target_energy', 0.5))
        
        # Calculate proximity: 1 - |song_energy - target_energy|
        energy_similarity = 1.0 - abs(song_energy - target_energy)
        
        # Clamp to [0.0, 1.0] to handle edge cases
        energy_similarity = max(0.0, min(1.0, energy_similarity))
        
        score += energy_similarity
        reasons.append(f"Energy similarity (+{energy_similarity:.2f})")
    
    except (KeyError, ValueError, TypeError):
        pass  # Gracefully handle missing or invalid energy data
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Score all songs and return the top K recommendations with explanations.
    
    Args:
        user_prefs (Dict): User preference profile
        songs (List[Dict]): List of song dictionaries
        k (int): Number of top recommendations to return (default 5)
    
    Returns:
        List[Tuple[Dict, float, List[str]]]: List of tuples containing:
                                             - song (Dict): The song dictionary
                                             - score (float): The composite score
                                             - reasons (List[str]): Justifications for the score
    """
    scored_songs = []
    
    # Score each song
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top K
    return scored_songs[:k]
