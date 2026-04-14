from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
        """
        Recommends the top k songs for a given user profile.
        """
        scored_songs = []
        for song in self.songs:
            score = self._compute_score(user, song)
            scored_songs.append((score, song))
        scored_songs.sort(key=lambda x: x[0], reverse=True)
        return [song for score, song in scored_songs[:k]]
        
    def _compute_score(self, user: UserProfile, song: Song) -> float:
        score = 0.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
        energy_diff = abs(song.energy - user.target_energy)
        score += max(0.0, 1.0 - energy_diff)
        if user.likes_acoustic and song.acousticness > 0.5:
            score += 0.5
        elif not user.likes_acoustic and song.acousticness <= 0.5:
            score += 0.5
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a given song might have been recommended to the user.
        """
        score = self._compute_score(user, song)
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("Genre matches perfectly (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("Mood matches (+1.0)")
        
        energy_score = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        reasons.append(f"Energy proximity (+{energy_score:.2f})")
        
        return f"Scored {score:.2f}. " + " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]:
                row[key] = float(row[key])
            row["id"] = int(row["id"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []
    
    if "genre" in user_prefs and song["genre"].lower() == user_prefs["genre"].lower():
        score += 2.0
        reasons.append(f"Genre match (+2.0)")
    
    if "mood" in user_prefs and song["mood"].lower() == user_prefs["mood"].lower():
        score += 1.0
        reasons.append(f"Mood match (+1.0)")
        
    if "energy" in user_prefs:
        energy_diff = abs(song["energy"] - user_prefs["energy"])
        energy_score = max(0.0, 1.0 - energy_diff)
        score += energy_score
        reasons.append(f"Energy proximity (+{energy_score:.2f})")
        
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))
        
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
