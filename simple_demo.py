#!/usr/bin/env python3
"""
Simple Demo for Agentic Mentor - AI-Driven Internal Knowledge Explorer
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def print_header():
    """Print demo header"""
    print("🤖" + "="*60 + "🤖")
    print("           AGENTIC MENTOR - AI-Driven Internal Knowledge Explorer")
    print("🤖" + "="*60 + "🤖")
    print()

def demo_use_cases():
    """Demonstrate use cases with examples"""
    print("🎯 USE CASES & EXAMPLES")
    print("-" * 50)
    
    use_cases = [
        {
            "title": "1. New Employee Onboarding",
            "scenario": "Sarah joins as a frontend developer",
            "query": "How do we handle authentication in our React apps?",
            "response": "Based on our codebase, we use Auth0 with custom hooks. Here's the pattern from project X, and here's why we chose this over Firebase...",
            "sources": ["GitHub: frontend-app/auth", "Confluence: Authentication Guide"]
        },
        {
            "title": "2. Project Context Switching",
            "scenario": "Mike moves from backend to frontend team",
            "query": "What's our state management strategy and why?",
            "response": "We use Redux Toolkit because [historical decision from Jira ticket #1234]. Here are the patterns we follow, and here's the migration guide from our old MobX setup...",
            "sources": ["Jira: TECH-1234", "GitHub: state-management", "Slack: tech-decisions"]
        },
        {
            "title": "3. Architecture Decisions",
            "scenario": "Team planning a new microservice",
            "query": "How do we handle database migrations in our microservices?",
            "response": "We use Flyway with this pattern [links to Confluence docs]. Here's why we chose this over Liquibase [links to decision log], and here are common pitfalls we've encountered...",
            "sources": ["Confluence: Database Standards", "Jira: ARCH-567", "GitHub: backend-app/db"]
        },
        {
            "title": "4. Bug Investigation",
            "scenario": "Developer debugging a production issue",
            "query": "Has anyone encountered this error before?",
            "response": "Yes, this was reported in Jira ticket #5678. The root cause was X, and here's the fix we implemented. Also check this related Slack thread for additional context...",
            "sources": ["Jira: BUG-5678", "Slack: #bugs", "GitHub: issue-123"]
        },
        {
            "title": "5. Best Practices Discovery",
            "scenario": "Developer starting a new feature",
            "query": "What's our testing strategy for API endpoints?",
            "response": "We use Jest with supertest. Here's our testing template, coverage requirements, and examples from similar endpoints. We also have these common patterns...",
            "sources": ["Confluence: Testing Strategy", "GitHub: test-templates", "Jira: TEST-456"]
        }
    ]
    
    for i, case in enumerate(use_cases, 1):
        print(f"\n{case['title']}")
        print(f"Scenario: {case['scenario']}")
        print(f"Query: \"{case['query']}\"")
        print(f"Agent Response: {case['response']}")
        print(f"Sources: {', '.join(case['sources'])}")
        print("-" * 30)

def demo_architecture():
    """Show the system architecture"""
    print("\n🏗️ SYSTEM ARCHITECTURE")
    print("-" * 50)
    
    architecture = """
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   API Gateway   │    │  Agent Manager  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Vector Store   │◄───│  Knowledge      │◄───│  Crawler Agents │
│  (Chroma/Pinecone) │    │  Processor     │    │  (GitHub, Jira, │
└─────────────────┘    └─────────────────┘    │  Confluence)     │
                                │             └─────────────────┘
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Memory System  │    │  Q&A Agent      │    │  Reflection     │
│  (Past Queries) │    │  (LLM + RAG)    │    │  Agent         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
"""
    print(architecture)

def demo_features():
    """Show key features"""
    print("\n🔧 KEY FEATURES")
    print("-" * 50)
    
    features = [
        "🤖 Multi-Agent Architecture - Specialized agents for different tasks",
        "🔍 Multi-Source Crawling - GitHub, Jira, Confluence, Slack",
        "🧠 Semantic Search & RAG - Vector-based knowledge retrieval",
        "💾 Memory Augmentation - Learns from past interactions",
        "🔄 Reflection & Improvement - Continuously improves response quality",
        "🌐 Beautiful Web Interface - Modern, responsive UI",
        "📊 Real-time Analytics - Performance metrics and insights",
        "🔒 Security & Privacy - Enterprise-grade security",
        "⚡ Async Architecture - Non-blocking operations",
        "📈 Scalable Design - Easy to extend with new sources"
    ]
    
    for feature in features:
        print(f"  {feature}")

def demo_agents():
    """Show the agent system"""
    print("\n🤖 AGENT SYSTEM")
    print("-" * 50)
    
    agents = [
        {
            "name": "Q&A Agent",
            "role": "Handles user queries with RAG",
            "capabilities": ["Semantic search", "Context-aware responses", "Source attribution"]
        },
        {
            "name": "Crawler Agent",
            "role": "Orchestrates knowledge extraction",
            "capabilities": ["Multi-source crawling", "Content processing", "Metadata extraction"]
        },
        {
            "name": "Memory Agent",
            "role": "Learns from interactions",
            "capabilities": ["Query history", "Response learning", "Pattern recognition"]
        },
        {
            "name": "Reflection Agent",
            "role": "Analyzes and improves responses",
            "capabilities": ["Quality assessment", "Response improvement", "Learning feedback"]
        }
    ]
    
    for agent in agents:
        print(f"\n{agent['name']}")
        print(f"  Role: {agent['role']}")
        print(f"  Capabilities: {', '.join(agent['capabilities'])}")

def demo_knowledge_sources():
    """Show knowledge sources"""
    print("\n📚 KNOWLEDGE SOURCES")
    print("-" * 50)
    
    sources = [
        {
            "name": "GitHub",
            "content": "Code, issues, pull requests, documentation",
            "integration": "GitHub API with token authentication"
        },
        {
            "name": "Jira",
            "content": "Project management, decisions, processes",
            "integration": "Jira REST API with OAuth"
        },
        {
            "name": "Confluence",
            "content": "Documentation, guides, knowledge base",
            "integration": "Confluence REST API"
        },
        {
            "name": "Slack",
            "content": "Team discussions, decisions, tribal knowledge",
            "integration": "Slack Web API with bot token"
        }
    ]
    
    for source in sources:
        print(f"\n{source['name']}")
        print(f"  Content: {source['content']}")
        print(f"  Integration: {source['integration']}")

def demo_benefits():
    """Show benefits"""
    print("\n🎯 BENEFITS")
    print("-" * 50)
    
    benefits = [
        "⏰ Save Hours - Find information in seconds instead of hours",
        "🧠 Reduce Cognitive Load - No need to remember where information is stored",
        "🔄 Faster Onboarding - New employees get productive in days, not weeks",
        "📈 Better Decisions - Access to historical context and reasoning",
        "🤝 Knowledge Sharing - Tribal knowledge becomes accessible to all",
        "🔍 Discoverability - Find related information you didn't know existed",
        "📊 Analytics - Understand what information is most valuable",
        "🔄 Continuous Learning - System improves over time",
        "🔒 Security - Enterprise-grade access controls",
        "🌐 Integration - Works with existing tools and workflows"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")

def demo_implementation():
    """Show implementation details"""
    print("\n🚀 IMPLEMENTATION")
    print("-" * 50)
    
    print("""
Quick Start:
1. Install dependencies: pip install -r requirements.txt
2. Configure environment: cp env.example .env
3. Run the demo: python demo.py
4. Start web interface: python main.py
5. Access at: http://localhost:8000

Configuration:
- Set up API keys for OpenAI, GitHub, Jira, etc.
- Configure knowledge sources in .env file
- Customize agent behavior and learning parameters

Deployment:
- Docker support for containerized deployment
- Kubernetes manifests for scalable deployment
- Monitoring and logging integration
- Backup and recovery procedures
""")

def main():
    """Run the demo"""
    print_header()
    
    demo_use_cases()
    demo_architecture()
    demo_features()
    demo_agents()
    demo_knowledge_sources()
    demo_benefits()
    demo_implementation()
    
    print("\n" + "="*60)
    print("🎉 Agentic Mentor Demo Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Configure your API keys in .env file")
    print("2. Run 'python main.py' to start the web interface")
    print("3. Access the system at http://localhost:8000")
    print("4. Start crawling your knowledge sources")
    print("5. Begin asking questions and learning from the system!")

if __name__ == "__main__":
    main() 