#!/usr/bin/env python3
"""
Script to populate the vector store with sample knowledge data
"""

import asyncio
import uuid
from datetime import datetime
from typing import List
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.models import KnowledgeChunk, SourceType
from src.knowledge.vector_store import VectorStore


async def populate_sample_data():
    """Populate the vector store with sample knowledge chunks"""
    
    print("🤖 Populating vector store with sample data...")
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Sample knowledge chunks
    sample_chunks = [
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="Agentic Mentor is an AI-driven internal knowledge explorer that helps employees quickly find and understand organizational knowledge scattered across various tools like GitHub, Jira, Confluence, and Slack. It uses semantic search and RAG (Retrieval-Augmented Generation) to provide accurate, contextual responses.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "system_overview", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="The system uses a multi-agent architecture with specialized agents: Q&A Agent for handling queries, Crawler Agent for knowledge extraction, Memory Agent for learning from interactions, and Reflection Agent for improving response quality.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "architecture", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="To run the project, activate the virtual environment with '.venv\\Scripts\\activate' and then run 'python run_server.py'. The web interface will be available at http://localhost:3000.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "setup", "importance": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="The system supports multiple LLM providers including OpenAI GPT-4, Google Gemini, and Grok. You can configure which provider to use by setting the appropriate API keys in the environment variables.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "configuration", "importance": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="The vector store uses ChromaDB for storing embeddings and sentence-transformers for generating embeddings. The system can crawl knowledge from GitHub repositories, Jira projects, Confluence spaces, and Slack channels.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "technical", "importance": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="Hello! I am Agentic Mentor, your AI-powered knowledge assistant. I can help you find information about your organization's knowledge base, answer questions about projects, and provide insights from various sources like GitHub, Jira, Confluence, and Slack.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "introduction", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="The system uses FastAPI for the web server, provides RESTful API endpoints for queries and crawling, and includes a beautiful web interface built with Tailwind CSS. It supports real-time analytics and comprehensive logging.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "technical", "importance": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="You can ask me questions about your organization's knowledge, such as 'How do we handle authentication?', 'What's our testing strategy?', or 'Show me recent project decisions'. I'll search through available sources and provide relevant answers.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "usage", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="Hello! I am Agentic Mentor, your AI assistant. I can help you find information, answer questions, and explore knowledge across your organization. How can I assist you today?",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "greeting", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="I am an AI-powered knowledge assistant designed to help you navigate and understand your organization's information. I can search across multiple sources and provide context-aware answers to your questions.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "introduction", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="The system uses advanced natural language processing and semantic search to understand your questions and find the most relevant information from your organization's knowledge base.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "technical", "importance": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="You can ask me questions about any topic related to your organization, and I'll search through available knowledge sources to provide you with accurate and helpful answers.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "usage", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="The system provides confidence scores for responses and can suggest follow-up questions to help you explore topics more deeply. It also maintains memory of your interactions to provide more personalized responses over time.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "features", "importance": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id=str(uuid.uuid4()),
            content="I am here to help you with any questions about your organization's knowledge base. Whether you need information about projects, processes, or general questions, I can assist you.",
            source_type=SourceType.MANUAL,
            source_id="system_docs",
            source_url="https://github.com/agentic-mentor",
            metadata={"category": "help", "importance": "high"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    try:
        # Add chunks to vector store
        chunk_ids = await vector_store.add_chunks(sample_chunks)
        
        print(f"✅ Successfully added {len(chunk_ids)} sample chunks to vector store")
        print("📊 Sample data includes:")
        for chunk in sample_chunks:
            print(f"  - {chunk.metadata.get('category', 'unknown')}: {chunk.content[:50]}...")
        
        # Get stats to verify
        stats = await vector_store.get_stats()
        print(f"📈 Vector store now contains {stats['total_chunks']} total chunks")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(populate_sample_data())
    if success:
        print("\n🎉 Sample data population completed successfully!")
        print("🚀 You can now test the system with queries like:")
        print("   - 'What is Agentic Mentor?'")
        print("   - 'How do I run the project?'")
        print("   - 'What LLM providers are supported?'")
    else:
        print("\n❌ Failed to populate sample data")
        sys.exit(1) 