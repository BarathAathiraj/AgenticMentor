#!/usr/bin/env python3
"""
Debug script for projects count
"""

import asyncio
import sys
import requests
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from populate_sample_data import populate_sample_data

async def debug_projects():
    """Debug the projects count functionality"""
    
    print("🔍 Debugging Projects Count")
    print("=" * 40)
    
    # Populate sample data
    print("\n📚 Populating sample data...")
    doc_count = await populate_sample_data()
    print(f"✅ Added {doc_count} documents")
    
    # Test the API
    print("\n🌐 Testing API...")
    try:
        response = requests.get("http://localhost:3000/api/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response:")
            print(f"   Documents: {data.get('documents', 0)}")
            print(f"   Projects: {data.get('repositories', 0)}")
            print(f"   Sources: {data.get('sources', 0)}")
            
            if data.get('repositories_list'):
                print(f"\n📋 Projects List:")
                for project in data['repositories_list']:
                    print(f"   - {project['name']}: {project['documents']} docs")
            else:
                print("❌ No projects list found")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:3000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_projects()) 