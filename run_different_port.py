#!/usr/bin/env python3
"""
Run Agentic Mentor on a different port
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_on_port(port=3000):
    """Run the system on a specific port"""
    
    # Set environment variables
    os.environ["WEB_PORT"] = str(port)
    os.environ["OPENAI_API_KEY"] = "demo_key"
    os.environ["SECRET_KEY"] = "demo-secret-key"
    os.environ["ENCRYPTION_KEY"] = "demo-encryption-key"
    
    print(f"🤖 Starting Agentic Mentor on port {port}")
    print(f"🌐 Access the system at: http://localhost:{port}")
    print("=" * 50)
    
    # Import and run the main application
    from src.main import AgenticMentor
    
    app = AgenticMentor()
    app.run()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Agentic Mentor on a specific port")
    parser.add_argument("--port", type=int, default=3000, help="Port to run the server on")
    
    args = parser.parse_args()
    
    run_on_port(args.port) 