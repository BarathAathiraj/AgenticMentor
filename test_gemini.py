#!/usr/bin/env python3
"""
Test Gemini API Integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_gemini_connection():
    """Test connection to Gemini API"""
    
    # Set environment for Gemini
    os.environ.update({
        "USE_GEMINI": "true",
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "demo_key")
    })
    
    try:
        from src.llm_client import LLMClient
        
        client = LLMClient()
        
        # Test message
        messages = [
            {"role": "user", "content": "Hello! Can you tell me a short joke?"}
        ]
        
        response = await client.call_llm(messages, temperature=0.7, max_tokens=100)
        
        print("✅ Gemini API connection successful!")
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        return False

async def test_agentic_mentor_query():
    """Test a simple query through the Agentic Mentor system"""
    
    url = "http://localhost:8000/api/query"
    
    payload = {
        "query": "What is the purpose of this system?",
        "user_id": "test_user"
    }
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Agentic Mentor query successful!")
                    print(f"Response: {result['response']}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Agentic Mentor API error: {response.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error connecting to Agentic Mentor: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Testing Gemini API and Agentic Mentor Connection")
    print("=" * 50)
    
    # Test Gemini connection
    print("\n1. Testing Gemini API connection...")
    gemini_success = await test_gemini_connection()
    
    if gemini_success:
        print("\n2. Testing Agentic Mentor query...")
        await test_agentic_mentor_query()
    else:
        print("\n❌ Skipping Agentic Mentor test - Gemini API not available")
        print("💡 Make sure to set your GEMINI_API_KEY environment variable!")

if __name__ == "__main__":
    asyncio.run(main()) 