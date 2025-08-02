#!/usr/bin/env python3
"""
Simple test to check ChromaDB contents without loading embedding model
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import chromadb
from chromadb.config import Settings

def test_chroma_directly():
    """Test ChromaDB directly without embedding model"""
    
    print("🔍 Testing ChromaDB Directly")
    print("=" * 40)
    
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(
            path="./data/chroma",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get the collection
        collection = client.get_or_create_collection("knowledge_chunks")
        
        # Get all data
        results = collection.get(include=['metadatas'])
        
        print(f"\n📊 ChromaDB Stats:")
        print(f"   Total chunks: {len(results['ids'])}")
        
        if len(results['ids']) > 0:
            print(f"\n📚 Sample Chunks:")
            for i in range(min(5, len(results['ids']))):
                print(f"   {i+1}. ID: {results['ids'][i][:8]}...")
                print(f"      Source ID: '{results['metadatas'][i].get('source_id', 'N/A')}'")
                print(f"      Source Type: '{results['metadatas'][i].get('source_type', 'N/A')}'")
                if results['documents'] and i < len(results['documents']):
                    print(f"      Content: {results['documents'][i][:50]}...")
                else:
                    print(f"      Content: [No document content]")
                print()
            
            # Test project extraction
            print("\n🔍 Testing Project Extraction:")
            project_groups = {}
            
            for i, metadata in enumerate(results['metadatas']):
                source_id = metadata.get('source_id', '')
                source_type = metadata.get('source_type', 'unknown')
                
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
                
            if len(project_groups) == 0:
                print("   ❌ No projects found!")
                print("\n🔍 Debugging source_id values:")
                for i, metadata in enumerate(results['metadatas'][:10]):
                    print(f"   {i+1}. source_id: '{metadata.get('source_id', 'N/A')}'")
                    print(f"      source_type: '{metadata.get('source_type', 'N/A')}'")
        else:
            print("   ❌ No chunks found in ChromaDB")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chroma_directly() 