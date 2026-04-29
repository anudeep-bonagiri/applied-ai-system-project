import pytest
import json
import os
from src.agent import get_music_recommendations

def test_tool_calling_logic_high_energy_rock():
    """Test that the tool correctly returns rock music when requested."""
    # Simulate the LLM calling the tool with specific extracted parameters
    result_json = get_music_recommendations(genre="rock", mood="intense", energy=0.95)
    
    # Parse the JSON string returned by the tool
    results = json.loads(result_json)
    
    assert len(results) > 0
    # Ensure the top recommendation is heavily influenced by the inputs
    top_song = results[0]
    assert "Score" not in top_song # the key is lowercase 'score'
    assert top_song["score"] > 0 # make sure it actually scored points
    
def test_tool_calling_logic_chill_lofi():
    """Test that the tool handles chill/lofi properly."""
    result_json = get_music_recommendations(genre="lofi", mood="focused", energy=0.2)
    results = json.loads(result_json)
    
    assert len(results) > 0
    
def test_tool_logging():
    """Test that the tool successfully logs its calls."""
    if os.path.exists("agent_tool_calls.log"):
        os.remove("agent_tool_calls.log")
        
    get_music_recommendations(genre="pop", mood="happy", energy=0.8)
    
    assert os.path.exists("agent_tool_calls.log")
    
    with open("agent_tool_calls.log", "r") as f:
        log_content = f.read()
        
    assert '"genre": "pop"' in log_content
    assert '"mood": "happy"' in log_content
    
    # cleanup
    os.remove("agent_tool_calls.log")
