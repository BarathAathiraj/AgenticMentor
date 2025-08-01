#!/usr/bin/env python3
"""
Simple Gemini API test without full application initialization
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_gemini_only():
    """Test only the Gemini API without other components"""
    
    print("🧪 Testing Gemini API Only")
    print("=" * 50)
    
    try:
        from src.llm_client import LLMClient
        
        # Set environment for Gemini
        os.environ["USE_GEMINI"] = "true"
        os.environ["GEMINI_API_KEY"] = "AIzaSyDaLNMhveJzhZHb43CvyfHJaaiGo7DZfTs"
        
        # Initialize client
        client = LLMClient()
        
        # Test with a simple query
        test_messages = [
            {"role": "user", "content": "Hello! Can you respond with 'Gemini is working!'?"}
        ]
        
        print("🔧 Testing Gemini connection...")
        response = await client.call_llm(test_messages)
        print(f"✅ Gemini Response: {response}")
        
        # Test with a more complex query
        complex_messages = [
            {"role": "user", "content": "What is 2 + 2? Please respond briefly."}
        ]
        
        print("\n🔧 Testing complex query...")
        response2 = await client.call_llm(complex_messages)
        print(f"✅ Complex Response: {response2}")
        
        print("\n🎉 Gemini API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🤖 Simple Gemini API Test")
    print("=" * 60)
    
    result = asyncio.run(test_gemini_only())
    
    print("\n" + "=" * 60)
    if result:
        print("🎉 Gemini API test passed!")
        print("🚀 You can now run the server with:")
        print("   python run_gemini.py --port 3000")
    else:
        print("❌ Gemini API test failed.")
    print("=" * 60) 