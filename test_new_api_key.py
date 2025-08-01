#!/usr/bin/env python3
"""
Test the new Gemini API key
"""

import os
import sys
from pathlib import Path

# Set environment variables
os.environ["GEMINI_API_KEY"] = "AIzaSyAlyO95cDTxdYivhmOtXGKLxXJWzKsYwrM"
os.environ["USE_GEMINI"] = "true"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_new_api_key():
    """Test the new API key"""
    
    print("🧪 Testing New Gemini API Key")
    print("=" * 50)
    
    try:
        from src.llm_client import LLMClient
        
        # Initialize client
        client = LLMClient()
        
        # Test with a simple query
        messages = [
            {"role": "user", "content": "Hello! Can you respond with 'API Key Test Successful'?"}
        ]
        
        print("🔧 Testing API connection...")
        response = await client.call_llm(messages, temperature=0.1)
        
        print(f"✅ Response: {response}")
        
        if "API Key Test Successful" in response or "Hello" in response:
            print("🎉 New API key is working correctly!")
            return True
        else:
            print("⚠️ API key works but response format is unexpected")
            return True
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_new_api_key())
    if success:
        print("\n🚀 Ready to start server!")
        print("Run: python simple_gemini_server.py")
    else:
        print("\n❌ API key test failed!") 