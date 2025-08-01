#!/usr/bin/env python3
"""
Demo script for Agentic Mentor
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.knowledge.vector_store import VectorStore
from src.knowledge.search import SemanticSearch
from src.agents.qa_agent import QAAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.reflection_agent import ReflectionAgent
from src.models import KnowledgeChunk, SourceType


async def create_sample_data():
    """Create sample knowledge chunks for demonstration"""
    
    print("🤖 Creating sample knowledge base...")
    
    # Initialize components
    vector_store = VectorStore()
    search_engine = SemanticSearch(vector_store)
    
    # Sample knowledge chunks
    sample_chunks = [
        KnowledgeChunk(
            id="auth-001",
            content="We use Auth0 for authentication across all our React applications. The implementation includes custom hooks for user management and role-based access control. Key files: src/hooks/useAuth.js, src/components/AuthProvider.jsx",
            source_type=SourceType.GITHUB,
            source_id="frontend-app/auth",
            source_url="https://github.com/company/frontend-app/blob/main/src/hooks/useAuth.js",
            metadata={"type": "code", "language": "javascript", "topic": "authentication"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="testing-001",
            content="Our testing strategy uses Jest with React Testing Library for frontend tests. We maintain 80% code coverage minimum. For API testing, we use supertest with custom test utilities. See: tests/api/helpers.js for common test patterns.",
            source_type=SourceType.CONFLUENCE,
            source_id="testing-guide",
            source_url="https://company.atlassian.net/wiki/spaces/TECH/pages/123456/Testing+Strategy",
            metadata={"type": "documentation", "topic": "testing"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="deployment-001",
            content="Deployment process: 1) Run tests in CI/CD pipeline 2) Build Docker image 3) Deploy to staging environment 4) Run integration tests 5) Deploy to production with blue-green deployment. See Jira ticket DEPLOY-123 for detailed process.",
            source_type=SourceType.JIRA,
            source_id="DEPLOY-123",
            source_url="https://company.atlassian.net/browse/DEPLOY-123",
            metadata={"type": "process", "topic": "deployment"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="database-001",
            content="Database migrations are handled with Flyway. We use versioned migration files in src/main/resources/db/migration/. Naming convention: V{version}__{description}.sql. Always test migrations in staging first.",
            source_type=SourceType.GITHUB,
            source_id="backend-app/db",
            source_url="https://github.com/company/backend-app/tree/main/src/main/resources/db/migration",
            metadata={"type": "code", "language": "sql", "topic": "database"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="slack-001",
            content="Team discussion: We decided to use Redux Toolkit instead of MobX for state management because it provides better TypeScript support and has a more predictable API. Migration guide available in Confluence.",
            source_type=SourceType.SLACK,
            source_id="tech-decisions",
            source_url="https://company.slack.com/archives/C1234567890/p1234567890",
            metadata={"type": "discussion", "topic": "state-management"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="api-001",
            content="API design follows RESTful principles with OpenAPI 3.0 specification. All endpoints return consistent JSON responses with error codes. Authentication via JWT tokens. Rate limiting: 1000 requests per hour per user.",
            source_type=SourceType.CONFLUENCE,
            source_id="api-standards",
            source_url="https://company.atlassian.net/wiki/spaces/API/pages/789012/API+Standards",
            metadata={"type": "documentation", "topic": "api"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="monitoring-001",
            content="We use Prometheus for metrics collection and Grafana for visualization. Key metrics: response time, error rate, throughput. Alerts configured for 5xx errors > 1% and response time > 2s.",
            source_type=SourceType.GITHUB,
            source_id="monitoring-setup",
            source_url="https://github.com/company/infrastructure/tree/main/monitoring",
            metadata={"type": "configuration", "topic": "monitoring"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    # Add chunks to vector store
    await vector_store.add_chunks(sample_chunks)
    
    print(f"✅ Added {len(sample_chunks)} sample knowledge chunks")
    return vector_store, search_engine


async def demo_qa_agent(search_engine):
    """Demonstrate Q&A agent capabilities"""
    
    print("\n🤖 Testing Q&A Agent...")
    
    qa_agent = QAAgent(None, search_engine)
    
    # Sample queries
    queries = [
        "How do we handle authentication in our applications?",
        "What's our testing strategy and tools?",
        "How does our deployment process work?",
        "What database migration tools do we use?",
        "What state management solution did we choose and why?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        
        try:
            result = await qa_agent.process({
                "query_text": query,
                "user_id": "demo_user",
                "context": {}
            })
            
            response = result["response"]
            print(f"🤖 Response: {response.response_text[:200]}...")
            print(f"📊 Confidence: {response.confidence_score:.2f}")
            print(f"🔗 Sources: {len(response.sources)} found")
            
        except Exception as e:
            print(f"❌ Error: {e}")


async def demo_memory_agent():
    """Demonstrate memory agent capabilities"""
    
    print("\n🧠 Testing Memory Agent...")
    
    memory_agent = MemoryAgent()
    
    # Simulate learning from interactions
    sample_interactions = [
        {
            "query": "How do we handle authentication?",
            "response": "We use Auth0 with custom hooks...",
            "satisfaction": 4
        },
        {
            "query": "What's our testing approach?",
            "response": "We use Jest with React Testing Library...",
            "satisfaction": 5
        },
        {
            "query": "How to deploy to production?",
            "response": "Follow the deployment checklist...",
            "satisfaction": 3
        }
    ]
    
    for interaction in sample_interactions:
        await memory_agent.process({
            "operation": "learn",
            "query": type('Query', (), {'id': 'demo', 'user_id': 'demo', 'query_text': interaction['query'], 'timestamp': datetime.utcnow()})(),
            "response": type('Response', (), {'response_text': interaction['response'], 'confidence_score': 0.8, 'sources': []})(),
            "satisfaction_score": interaction['satisfaction']
        })
    
    # Get memory stats
    stats = await memory_agent.get_memory_stats()
    print(f"📊 Memory Stats: {stats['total_memories']} memories, Avg satisfaction: {stats['average_satisfaction']:.2f}")


async def demo_reflection_agent():
    """Demonstrate reflection agent capabilities"""
    
    print("\n🔍 Testing Reflection Agent...")
    
    reflection_agent = ReflectionAgent()
    
    # Sample response to analyze
    sample_query = type('Query', (), {'query_text': 'How do we handle authentication?'})()
    sample_response = type('Response', (), {
        'response_text': 'We use Auth0 for authentication. It provides JWT tokens and handles user sessions.',
        'confidence_score': 0.7,
        'sources': []
    })()
    
    # Analyze response
    analysis = await reflection_agent.process({
        "operation": "analyze",
        "query": sample_query,
        "response": sample_response,
        "search_results": []
    })
    
    print(f"📊 Analysis: Quality score {analysis['quality_score']:.2f}")
    print(f"✅ Strengths: {', '.join(analysis['strengths'])}")
    print(f"🔧 Improvements: {', '.join(analysis['improvement_areas'])}")


async def demo_search_capabilities(search_engine):
    """Demonstrate search capabilities"""
    
    print("\n🔍 Testing Search Capabilities...")
    
    # Test different search types
    search_tests = [
        ("authentication", "Basic semantic search"),
        ("testing", "Search by topic"),
        ("deployment", "Process-related search")
    ]
    
    for query, description in search_tests:
        print(f"\n🔎 {description}: '{query}'")
        
        results = await search_engine.search(query, limit=3)
        
        for i, result in enumerate(results, 1):
            chunk = result.chunk
            print(f"  {i}. {chunk.source_type.value}: {chunk.content[:100]}... (similarity: {result.similarity_score:.2f})")


async def main():
    """Run the complete demo"""
    
    print("🚀 Starting Agentic Mentor Demo")
    print("=" * 50)
    
    try:
        # Create sample data
        vector_store, search_engine = await create_sample_data()
        
        # Demo different components
        await demo_search_capabilities(search_engine)
        await demo_qa_agent(search_engine)
        await demo_memory_agent()
        await demo_reflection_agent()
        
        print("\n" + "=" * 50)
        print("✅ Demo completed successfully!")
        print("\n🎯 Key Features Demonstrated:")
        print("• Semantic search across multiple knowledge sources")
        print("• Intelligent Q&A with confidence scoring")
        print("• Memory system for learning from interactions")
        print("• Reflection agent for response improvement")
        print("• Multi-source knowledge integration (GitHub, Jira, Confluence, Slack)")
        
        print("\n🚀 To start the web interface:")
        print("1. Copy env.example to .env and configure your API keys")
        print("2. Run: python main.py")
        print("3. Open: http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 