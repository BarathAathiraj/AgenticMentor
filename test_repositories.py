#!/usr/bin/env python3
"""
Test script for repository tracking feature
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from populate_sample_data import populate_sample_data

async def test_repositories():
    """Test the repository tracking feature"""
    
    print("🧪 Testing Repository Tracking Feature")
    print("=" * 50)
    
    # Populate sample data
    doc_count = await populate_sample_data()
    
    print(f"\n✅ Sample data populated: {doc_count} documents")
    print("\n📊 Expected repositories:")
    print("   - frontend-app (2 docs)")
    print("   - backend-app (1 doc)")
    print("   - company/infrastructure (1 doc)")
    print("   - Agentic-mentor (1 doc)")
    print("   - Fitness-Agent-A-Agentic-AI-Project (1 doc)")
    print("   - testing-guide (1 doc)")
    print("   - DEPLOY-123 (1 doc)")
    print("   - tech-decisions (1 doc)")
    print("   - api-standards (1 doc)")
    print("   - security-guide (1 doc)")
    
    print("\n🚀 Now you can:")
    print("   1. Start the server: python run_server.py")
    print("   2. Open http://localhost:3000/chat")
    print("   3. Click on the 'Repos: X' card in the top right")
    print("   4. See the list of repositories that have been read")
    
    return doc_count

if __name__ == "__main__":
    asyncio.run(test_repositories()) 