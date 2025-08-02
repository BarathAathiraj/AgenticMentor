#!/usr/bin/env python3
"""
Knowledge Base Setup Script for Agentic Mentor
Helps users populate their knowledge base with organizational data
"""

import os
import asyncio
from pathlib import Path
from src.knowledge.vector_store import VectorStore
from src.knowledge.crawlers import GitHubCrawler, JiraCrawler, ConfluenceCrawler
from src.config import settings

class KnowledgeBaseSetup:
    """Setup and populate the knowledge base with organizational data"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        
    async def setup_sample_data(self):
        """Add sample organizational data for testing"""
        print("📚 Setting up sample knowledge base...")
        
        sample_data = [
            {
                "content": "Our authentication strategy uses OAuth 2.0 with JWT tokens. All API endpoints require valid authentication headers.",
                "source_type": "documentation",
                "source_url": "https://docs.company.com/auth",
                "metadata": {"department": "security", "priority": "high"}
            },
            {
                "content": "Deployment process: 1) Run tests 2) Build Docker image 3) Deploy to staging 4) Run integration tests 5) Deploy to production",
                "source_type": "process",
                "source_url": "https://confluence.company.com/deployment",
                "metadata": {"department": "devops", "priority": "medium"}
            },
            {
                "content": "Code review guidelines: All PRs must have at least 2 approvals, pass all tests, and follow coding standards.",
                "source_type": "policy",
                "source_url": "https://github.com/company/repo/pull/123",
                "metadata": {"department": "engineering", "priority": "high"}
            }
        ]
        
        for item in sample_data:
            await self.vector_store.add_chunk(
                content=item["content"],
                source_type=item["source_type"],
                source_url=item["source_url"],
                metadata=item["metadata"]
            )
        
        print(f"✅ Added {len(sample_data)} sample documents")
    
    async def setup_github_integration(self, repo_url: str, token: str):
        """Setup GitHub repository crawling"""
        print(f"🔗 Setting up GitHub integration for {repo_url}")
        
        crawler = GitHubCrawler(token)
        await crawler.crawl_repository(repo_url)
        
        print("✅ GitHub integration complete")
    
    async def setup_jira_integration(self, server_url: str, username: str, token: str):
        """Setup Jira integration"""
        print(f"🔗 Setting up Jira integration for {server_url}")
        
        crawler = JiraCrawler(server_url, username, token)
        await crawler.crawl_projects()
        
        print("✅ Jira integration complete")
    
    async def setup_confluence_integration(self, server_url: str, username: str, token: str):
        """Setup Confluence integration"""
        print(f"🔗 Setting up Confluence integration for {server_url}")
        
        crawler = ConfluenceCrawler(server_url, username, token)
        await crawler.crawl_spaces()
        
        print("✅ Confluence integration complete")
    
    async def run_setup(self):
        """Run the complete knowledge base setup"""
        print("🚀 Starting Agentic Mentor Knowledge Base Setup")
        print("=" * 50)
        
        # 1. Setup sample data
        await self.setup_sample_data()
        
        # 2. Setup integrations (if configured)
        if settings.github_token:
            print("\n📋 GitHub Integration:")
            print("Enter your GitHub repository URL (or press Enter to skip):")
            repo_url = input().strip()
            if repo_url:
                await self.setup_github_integration(repo_url, settings.github_token)
        
        if settings.jira_api_token:
            print("\n📋 Jira Integration:")
            print("Enter your Jira server URL (or press Enter to skip):")
            server_url = input().strip()
            if server_url:
                await self.setup_jira_integration(server_url, settings.jira_username, settings.jira_api_token)
        
        if settings.confluence_api_token:
            print("\n📋 Confluence Integration:")
            print("Enter your Confluence server URL (or press Enter to skip):")
            server_url = input().strip()
            if server_url:
                await self.setup_confluence_integration(server_url, settings.confluence_username, settings.confluence_api_token)
        
        print("\n🎉 Knowledge base setup complete!")
        print("Your Agentic Mentor is now ready to answer questions about your organization!")

async def main():
    """Main setup function"""
    setup = KnowledgeBaseSetup()
    await setup.run_setup()

if __name__ == "__main__":
    asyncio.run(main()) 