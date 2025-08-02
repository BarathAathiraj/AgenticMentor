#!/usr/bin/env python3
"""
Analytics Dashboard for Agentic Mentor
Provides insights into knowledge usage, gaps, and organizational patterns
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict
from src.knowledge.vector_store import VectorStore
from src.config import settings

class AnalyticsDashboard:
    """Analytics dashboard for Agentic Mentor insights"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        
    async def get_usage_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for the specified period"""
        # This would typically query a database
        # For now, return sample data
        return {
            "total_queries": 1250,
            "unique_users": 45,
            "avg_response_time": 2.3,
            "top_questions": [
                "What is our authentication strategy?",
                "How do we handle deployments?",
                "What are our coding standards?",
                "Show me recent project decisions",
                "How do I set up the development environment?"
            ],
            "knowledge_sources": {
                "github": 450,
                "jira": 320,
                "confluence": 280,
                "slack": 200
            },
            "confidence_scores": {
                "high": 65,
                "medium": 25,
                "low": 10
            }
        }
    
    async def get_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """Identify knowledge gaps based on unanswered questions"""
        gaps = [
            {
                "topic": "Microservices Architecture",
                "frequency": 15,
                "last_asked": "2024-01-15",
                "suggested_sources": ["Architecture docs", "System design reviews"],
                "priority": "high"
            },
            {
                "topic": "Security Best Practices",
                "frequency": 12,
                "last_asked": "2024-01-12",
                "suggested_sources": ["Security guidelines", "Compliance docs"],
                "priority": "high"
            },
            {
                "topic": "Performance Optimization",
                "frequency": 8,
                "last_asked": "2024-01-10",
                "suggested_sources": ["Performance guides", "Monitoring docs"],
                "priority": "medium"
            }
        ]
        return gaps
    
    async def get_popular_topics(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get most popular topics and questions"""
        topics = [
            {
                "topic": "Authentication & Security",
                "query_count": 45,
                "avg_confidence": 0.85,
                "trend": "increasing"
            },
            {
                "topic": "Deployment & DevOps",
                "query_count": 38,
                "avg_confidence": 0.78,
                "trend": "stable"
            },
            {
                "topic": "Code Standards & Reviews",
                "query_count": 32,
                "avg_confidence": 0.92,
                "trend": "increasing"
            },
            {
                "topic": "Project Management",
                "query_count": 28,
                "avg_confidence": 0.75,
                "trend": "stable"
            },
            {
                "topic": "System Architecture",
                "query_count": 22,
                "avg_confidence": 0.68,
                "trend": "decreasing"
            }
        ]
        return topics
    
    async def get_user_insights(self) -> Dict[str, Any]:
        """Get insights about user behavior and patterns"""
        return {
            "active_users": {
                "daily": 12,
                "weekly": 35,
                "monthly": 45
            },
            "peak_usage_times": [
                {"hour": 9, "queries": 45},
                {"hour": 10, "queries": 52},
                {"hour": 11, "queries": 38},
                {"hour": 14, "queries": 41},
                {"hour": 15, "queries": 48},
                {"hour": 16, "queries": 35}
            ],
            "department_usage": {
                "engineering": 45,
                "product": 25,
                "design": 15,
                "marketing": 10,
                "other": 5
            },
            "query_complexity": {
                "simple": 60,
                "moderate": 30,
                "complex": 10
            }
        }
    
    async def get_knowledge_health_score(self) -> Dict[str, Any]:
        """Calculate overall knowledge health score"""
        return {
            "overall_score": 78,
            "components": {
                "coverage": 75,
                "accuracy": 82,
                "accessibility": 80,
                "freshness": 75
            },
            "recommendations": [
                "Add more documentation for microservices architecture",
                "Update security guidelines with latest best practices",
                "Create more visual guides for complex processes",
                "Implement automated knowledge freshness checks"
            ]
        }
    
    async def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "period": "Last 30 days",
            "usage_stats": await self.get_usage_statistics(),
            "knowledge_gaps": await self.get_knowledge_gaps(),
            "popular_topics": await self.get_popular_topics(),
            "user_insights": await self.get_user_insights(),
            "knowledge_health": await self.get_knowledge_health_score()
        }

class DashboardAPI:
    """API endpoints for analytics dashboard"""
    
    def __init__(self):
        self.dashboard = AnalyticsDashboard()
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all dashboard data"""
        return await self.dashboard.generate_report()
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return await self.dashboard.get_usage_statistics()
    
    async def get_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """Get knowledge gaps"""
        return await self.dashboard.get_knowledge_gaps()
    
    async def get_popular_topics(self) -> List[Dict[str, Any]]:
        """Get popular topics"""
        return await self.dashboard.get_popular_topics()
    
    async def get_health_score(self) -> Dict[str, Any]:
        """Get knowledge health score"""
        return await self.dashboard.get_knowledge_health_score()

# Example usage
async def main():
    """Example of using the analytics dashboard"""
    dashboard = AnalyticsDashboard()
    
    print("📊 Agentic Mentor Analytics Dashboard")
    print("=" * 50)
    
    # Get comprehensive report
    report = await dashboard.generate_report()
    
    print(f"\n📈 Usage Statistics:")
    stats = report["usage_stats"]
    print(f"  • Total Queries: {stats['total_queries']}")
    print(f"  • Unique Users: {stats['unique_users']}")
    print(f"  • Avg Response Time: {stats['avg_response_time']}s")
    
    print(f"\n🔍 Knowledge Gaps:")
    gaps = report["knowledge_gaps"]
    for gap in gaps[:3]:
        print(f"  • {gap['topic']} (Priority: {gap['priority']})")
    
    print(f"\n🏆 Popular Topics:")
    topics = report["popular_topics"]
    for topic in topics[:3]:
        print(f"  • {topic['topic']}: {topic['query_count']} queries")
    
    print(f"\n💡 Knowledge Health Score: {report['knowledge_health']['overall_score']}/100")

if __name__ == "__main__":
    asyncio.run(main()) 