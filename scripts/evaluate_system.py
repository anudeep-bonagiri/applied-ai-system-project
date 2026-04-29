import os
import sys
from dotenv import load_dotenv

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agent import MusicDJAgent

def evaluate():
    load_dotenv()
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY not found. Please set it before running evaluations.")
        return

    print("========================================")
    print("🚀 Running AI DJ Test Harness")
    print("========================================\\n")
    
    agent = MusicDJAgent()
    
    test_cases = [
        {"input": "I need some intense workout rock music.", "expected_tool": "get_music_recommendations"},
        {"input": "Give me some acoustic indie folk.", "expected_tool": "get_music_recommendations"},
        {"input": "Any chill synthwave?", "expected_tool": "get_music_recommendations"}
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}/{total}: '{test['input']}'")
        try:
            # We clear history for each test to keep it independent
            agent = MusicDJAgent()
            response, tools_used = agent.send_message(test['input'])
            
            # Checks
            tool_check = any(test['expected_tool'] in t for t in tools_used)
            tone_check = any(slang in response.lower() for slang in ['banger', 'vibes', 'no cap', 'slaps', 'w'])
            
            if tool_check and tone_check:
                print("✅ PASS: Tools called successfully AND persona tone maintained.")
                passed += 1
            elif not tool_check:
                print("❌ FAIL: Agent failed to call the expected tools.")
            elif not tone_check:
                print("❌ FAIL: Agent lost its Gen-Z DJ persona.")
                
        except Exception as e:
            print(f"❌ FAIL: Exception occurred - {e}")
        print("-" * 40)
        
    print(f"\\n📊 SUMMARY: {passed}/{total} tests passed. ({(passed/total)*100:.0f}%)")
    
if __name__ == "__main__":
    evaluate()
