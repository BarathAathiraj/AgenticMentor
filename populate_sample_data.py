#!/usr/bin/env python3
"""
Populate sample data for Agentic Mentor
Adds sample repository information to the knowledge base
"""

import asyncio
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.knowledge.vector_store import VectorStore
from src.models import KnowledgeChunk, SourceType

async def populate_sample_data():
    """Populate the knowledge base with sample repository data"""
    
    print("📚 Populating Agentic Mentor with sample repository data...")
    
    vector_store = VectorStore()
    
    # Sample repository data based on your GitHub profile
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
        ),
        KnowledgeChunk(
            id="agentic-mentor-001",
            content="Agentic Mentor is an AI-powered internal knowledge explorer that helps employees find and understand organizational knowledge scattered across various tools like GitHub, Jira, Confluence, Slack, and email.",
            source_type=SourceType.GITHUB,
            source_id="Agentic-mentor",
            source_url="https://github.com/maniselvam-v/Agentic-mentor",
            metadata={"type": "project", "language": "python", "topic": "ai-knowledge"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="fitness-agent-001",
            content="Fitness Agent is an AI-powered fitness application that provides personalized workout recommendations, health tracking, and nutrition guidance. Features include ML models for personalization and React Native mobile apps.",
            source_type=SourceType.GITHUB,
            source_id="Fitness-Agent-A-Agentic-AI-Project",
            source_url="https://github.com/maniselvam-v/Fitness-Agent-A-Agentic-AI-Project",
            metadata={"type": "project", "language": "python", "topic": "fitness-ai"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        KnowledgeChunk(
            id="security-001",
            content="Security best practices: 1) Use environment variables for secrets 2) Implement rate limiting 3) Validate all inputs 4) Use HTTPS everywhere 5) Regular security audits 6) Keep dependencies updated.",
            source_type=SourceType.CONFLUENCE,
            source_id="security-guide",
            source_url="https://company.atlassian.net/wiki/spaces/SEC/pages/456789/Security+Best+Practices",
            metadata={"type": "documentation", "topic": "security"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    try:
        # Add chunks to vector store
        chunk_ids = await vector_store.add_chunks(sample_chunks)
        
        print(f"✅ Successfully added {len(chunk_ids)} sample documents to the knowledge base!")
        print(f"📊 Document count: {len(chunk_ids)}")
        print(f"🔍 You can now ask questions about:")
        print(f"   - Authentication (Auth0 implementation)")
        print(f"   - Testing strategies (Jest, React Testing Library)")
        print(f"   - Deployment processes")
        print(f"   - Database migrations (Flyway)")
        print(f"   - State management (Redux Toolkit)")
        print(f"   - API design standards")
        print(f"   - Monitoring setup (Prometheus/Grafana)")
        print(f"   - Security best practices")
        print(f"   - Agentic Mentor project details")
        print(f"   - Fitness Agent project details")
        
        return len(chunk_ids)
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
        return 0

if __name__ == "__main__":
    asyncio.run(populate_sample_data()) 