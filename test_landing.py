#!/usr/bin/env python3
"""
Test script to verify the landing page is working
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_landing_page():
    """Test if the landing page template exists and is accessible"""
    
    # Set environment variables
    os.environ.update({
        "WEB_PORT": "3000",
        "OPENAI_API_KEY": "demo_key",
        "SECRET_KEY": "demo-secret-key",
        "ENCRYPTION_KEY": "demo-encryption-key",
        "WEB_HOST": "0.0.0.0",
        "WEB_DEBUG": "false",
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "./logs/agentic_mentor.log",
        "VECTOR_STORE_TYPE": "chroma",
        "CHROMA_PERSIST_DIRECTORY": "./data/chroma",
        "DATABASE_URL": "sqlite:///./data/agentic_mentor.db",
        "REDIS_URL": "redis://localhost:6379",
        "AGENT_MEMORY_SIZE": "1000",
        "AGENT_REFLECTION_ENABLED": "true",
        "AGENT_LEARNING_RATE": "0.1"
    })
    
    try:
        from src.main import AgenticMentor
        
        # Create the application
        app = AgenticMentor()
        
        # Test if templates are loaded
        print("✅ Templates loaded successfully")
        print(f"📁 Template directory: {app.templates.directory}")
        
        # Test if landing page template exists
        landing_template = Path("templates/landing.html")
        if landing_template.exists():
            print("✅ Landing page template exists")
            print(f"📄 Template size: {landing_template.stat().st_size} bytes")
        else:
            print("❌ Landing page template not found")
        
        # Test if chat template exists
        chat_template = Path("templates/index.html")
        if chat_template.exists():
            print("✅ Chat template exists")
            print(f"📄 Template size: {chat_template.stat().st_size} bytes")
        else:
            print("❌ Chat template not found")
        
        print("\n🚀 Starting server...")
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_landing_page() 