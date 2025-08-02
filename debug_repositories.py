#!/usr/bin/env python3
"""
Debug the _get_repositories_info method directly
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import AgenticMentor

async def debug_repositories():
    """Debug the repositories info method"""
    
    print("🔍 Debugging _get_repositories_info")
    print("=" * 40)
    
    try:
        # Create app instance
        app = AgenticMentor()
        
        # Test the method directly
        repositories = await app._get_repositories_info()
        
        print(f"\n📊 Results:")
        print(f"   Total repositories found: {len(repositories)}")
        
        if repositories:
            print(f"   Repositories:")
            for i, repo in enumerate(repositories[:5]):
                print(f"   - {i+1}. {repo['name']}: {repo['documents']} docs ({repo['source_type']})")
        else:
            print("   ❌ No repositories found!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_repositories()) 