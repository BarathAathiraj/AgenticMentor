#!/usr/bin/env python3
"""
Test script for Gemini API setup
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_gemini_setup():
    """Test the Gemini setup"""
    
    print("🧪 Testing Gemini API Setup")
    print("=" * 50)
    
    # Check environment variables
    gemini_key = os.getenv("GEMINI_API_KEY")
    use_gemini = os.getenv("USE_GEMINI", "false").lower() == "true"
    
    print(f"✅ USE_GEMINI: {use_gemini}")
    print(f"✅ GEMINI_API_KEY: {'Set' if gemini_key and gemini_key != 'your_gemini_api_key_here' else 'Not set or invalid'}")
    
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        print("\n❌ Please set your Gemini API key:")
        print("1. Get your key from: https://makersuite.google.com/app/apikey")
        print("2. Edit the .env file and replace 'your_gemini_api_key_here'")
        print("3. Or set environment variable: set GEMINI_API_KEY=your_key")
        return False
    
    # Test LLM client
    try:
        from src.llm_client import LLMClient
        
        print("\n🔧 Initializing LLM Client...")
        client = LLMClient()
        
        # Check client status
        status = client.get_status()
        print(f"✅ Provider: {status['provider']}")
        print(f"✅ Model: {status['model']}")
        print(f"✅ Status: {status['status']}")
        print(f"✅ API Key Configured: {status['api_key_configured']}")
        
        if status['provider'] == 'gemini' and status['api_key_configured']:
            print("\n🎉 Gemini is properly configured!")
            return True
        else:
            print(f"\n❌ Expected Gemini but got: {status['provider']}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error testing LLM client: {e}")
        return False

def test_web_server():
    """Test if the web server can start"""
    
    print("\n🌐 Testing Web Server Setup")
    print("=" * 50)
    
    try:
        from src.main import AgenticMentor
        
        print("✅ AgenticMentor class imported successfully")
        print("✅ All dependencies are available")
        
        # Test configuration
        from src.config import settings
        print(f"✅ Web Host: {settings.web_host}")
        print(f"✅ Web Port: {settings.web_port}")
        print(f"✅ Log Level: {settings.log_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing web server: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Agentic Mentor - Gemini Setup Test")
    print("=" * 60)
    
    # Test Gemini setup
    gemini_ok = test_gemini_setup()
    
    # Test web server
    server_ok = test_web_server()
    
    print("\n" + "=" * 60)
    if gemini_ok and server_ok:
        print("🎉 All tests passed! You're ready to run:")
        print("   python run_gemini.py")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        if not gemini_ok:
            print("   - Set your Gemini API key")
        if not server_ok:
            print("   - Check dependencies and configuration")
    
    print("=" * 60) 