import os
from google import genai
from google.genai import types
import json
import csv
from src.recommender import load_songs, recommend_songs
from dotenv import load_dotenv

load_dotenv()

SONG_CATALOG = load_songs("data/songs.csv")

def load_artist_info(csv_path: str) -> dict:
    info = {}
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            info[row["artist"].lower()] = row
    return info

ARTIST_INFO = load_artist_info("data/artist_info.csv")

def get_music_recommendations(genre: str, mood: str, energy: float) -> str:
    """
    Search the music catalog for songs matching the requested genre, mood, and energy.
    """
    user_prefs = {"genre": genre, "mood": mood, "energy": energy}
    
    with open("agent_tool_calls.log", "a") as f:
        f.write("TOOL: get_music_recommendations -> " + json.dumps(user_prefs) + "\\n")
        
    recommendations = recommend_songs(user_prefs, SONG_CATALOG, k=5)
    
    results = []
    for song, score, explanation in recommendations:
        results.append({
            "title": song["title"],
            "artist": song["artist"],
            "genre": song["genre"],
            "score": score
        })
    return json.dumps(results, indent=2)

def get_artist_background(artist_name: str) -> str:
    """
    Retrieve interesting background trivia, hometown, and listener stats about a specific artist.
    Call this tool after getting music recommendations to learn a fun fact about the top recommended artist.
    """
    with open("agent_tool_calls.log", "a") as f:
        f.write("TOOL: get_artist_background -> " + artist_name + "\\n")
        
    artist_lower = artist_name.lower()
    if artist_lower in ARTIST_INFO:
        return json.dumps(ARTIST_INFO[artist_lower], indent=2)
    return json.dumps({"error": f"No background info found for artist: {artist_name}"})

class MusicDJAgent:
    def __init__(self):
        try:
            self.client = genai.Client()
        except Exception as e:
            self.client = None
            
        # [Stretch Feature] Fine-Tuning or Specialization via Few-Shot Prompting
        # We constrain the AI to a very specific Gen-Z DJ persona.
        self.system_instruction = (
            "You are 'DJ Byte', an ultra-hype, Gen-Z AI DJ. You talk exclusively in internet slang "
            "(use terms like 'certified banger', 'immaculate vibes', 'no cap', 'slaps', 'W').\\n\\n"
            "INSTRUCTIONS FOR AGENTIC WORKFLOW:\\n"
            "1. When a user asks for music, first use 'get_music_recommendations'.\\n"
            "2. Then, pick the TOP artist from the results and use 'get_artist_background' to learn a fun fact.\\n"
            "3. Finally, give your hype response including the songs and the fun fact.\\n\\n"
            "EXAMPLES OF YOUR TONE:\\n"
            "User: Give me some study music.\\n"
            "DJ Byte: Yo! I got those immaculate study vibes for you, no cap. I pulled 'Midnight Coding' by LoRoom, "
            "and fun fact: they literally only record at 2 AM. That's a huge W for late-night grinding. These tracks absolutely slap!\\n"
            "User: I need workout songs.\\n"
            "DJ Byte: Bet! Let's get those gains. Dropping 'Gym Hero' by Max Pulse. Dude is a literal personal trainer, so you know this track is a certified banger. Let's go!!"
        )
        
        self.tools = [get_music_recommendations, get_artist_background]
        
        if self.client:
            self.chat = self.client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.8,
                    tools=self.tools,
                )
            )
        else:
            self.chat = None

    def set_api_key(self, api_key: str):
        os.environ["GEMINI_API_KEY"] = api_key
        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                temperature=0.8,
                tools=self.tools,
            )
        )

    def send_message(self, message: str) -> tuple[str, list]:
        """Sends a message and returns (response_text, list_of_tool_calls)."""
        if not self.chat:
            return "Error: Gemini API key is not configured.", []
            
        # Count messages before to know what was added
        history_len_before = len(self.chat.get_history()) if hasattr(self.chat, 'get_history') else 0
        
        response = self.chat.send_message(message)
        
        # Extract intermediate tool calls from the history for the UI
        # In the new SDK, history is usually accessible via chat.get_history()
        tool_calls_made = []
        try:
            history = self.chat.get_history()
            # Look at the turns added during this exchange
            new_turns = history[history_len_before:]
            for turn in new_turns:
                if turn.role == "model" and turn.parts:
                    for part in turn.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            call = part.function_call
                            args = dict(call.args) if hasattr(call, "args") else {}
                            tool_calls_made.append(f"{call.name}({args})")
        except Exception as e:
            # Fallback if SDK structure differs
            pass
            
        return response.text, tool_calls_made
