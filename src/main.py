"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs
from tabulate import tabulate


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs from the catalog.\n")

    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "Chill Lofi Study": {"genre": "lofi", "mood": "focused", "energy": 0.3},
        "Intense Workout Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
        "Adversarial (Conflicting)": {"genre": "classical", "mood": "focused", "energy": 0.99} 
    }

    for name, user_prefs in profiles.items():
        print(f"\n======================================")
        print(f"Profile: {name}")
        print(f"Prefs: {user_prefs}")
        print(f"======================================")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        
        table_data = []
        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            table_data.append([
                i, 
                song['title'], 
                song['artist'], 
                f"{score:.2f}", 
                explanation
            ])
            
        print(tabulate(table_data, headers=["Rank", "Title", "Artist", "Score", "Reasons"], tablefmt="fancy_grid"))
        print()

if __name__ == "__main__":
    main()
