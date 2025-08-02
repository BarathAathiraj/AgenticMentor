#!/usr/bin/env python3
"""
Test script to check vector store contents
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.knowledge.vector_store import VectorStore

async def test_vector_store():
    """Test the vector store contents"""
    
    print("🔍 Testing Vector Store Contents")
    print("=" * 40)
    
    vector_store = VectorStore()
    
    # Get stats
    stats = await vector_store.get_stats()
    print(f"\n📊 Vector Store Stats:")
    print(f"   Total chunks: {stats.get('total_chunks', 0)}")
    print(f"   Source types: {stats.get('source_type_distribution', {})}")
    
    # Get all chunks
    chunks = await vector_store.get_all_chunks()
    print(f"\n📚 All Chunks ({len(chunks)}):")
    
    for i, chunk in enumerate(chunks[:10]):  # Show first 10
        print(f"   {i+1}. ID: {chunk['id'][:8]}...")
        print(f"      Source ID: '{chunk['source_id']}'")
        print(f"      Source Type: '{chunk['source_type']}'")
        print(f"      Content: {chunk['content'][:50]}...")
        print()
    
    if len(chunks) > 10:
        print(f"   ... and {len(chunks) - 10} more chunks")
    
    # Test project extraction
    print("\n🔍 Testing Project Extraction:")
    project_groups = {}
    
    for chunk in chunks:
        source_id = chunk.get("source_id", "")
        source_type = chunk.get("source_type", "unknown")
        
        # Extract project name
        if "/" in source_id:
            project_name = source_id.split("/")[0]
        else:
            project_name = source_id
        
        if project_name and project_name != "" and project_name != "unknown":
            if project_name not in project_groups:
                project_groups[project_name] = {
                    "name": project_name,
                    "documents": 0,
                    "source_type": source_type
                }
            project_groups[project_name]["documents"] += 1
    
    print(f"   Found {len(project_groups)} projects:")
    for project_name, info in project_groups.items():
        print(f"   - {project_name}: {info['documents']} docs ({info['source_type']})")

if __name__ == "__main__":
    asyncio.run(test_vector_store()) 