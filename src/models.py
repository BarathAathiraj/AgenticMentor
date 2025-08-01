"""
Data models for Agentic Mentor
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class SourceType(str, Enum):
    """Types of knowledge sources"""
    GITHUB = "github"
    JIRA = "jira"
    CONFLUENCE = "confluence"
    SLACK = "slack"
    EMAIL = "email"
    MANUAL = "manual"


class KnowledgeChunk(BaseModel):
    """A chunk of knowledge from any source"""
    id: str
    content: str
    source_type: SourceType
    source_id: str
    source_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    embedding: Optional[List[float]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Query(BaseModel):
    """A user query to the agent"""
    id: str
    user_id: str
    query_text: str
    context: Optional[Dict[str, Any]] = None
    timestamp: datetime
    response: Optional[str] = None
    satisfaction_score: Optional[int] = None
    feedback: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentMemory(BaseModel):
    """Memory entry for the agent"""
    id: str
    query_id: str
    user_id: str
    query_text: str
    response: str
    satisfaction_score: Optional[int] = None
    learned_patterns: List[str] = Field(default_factory=list)
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchResult(BaseModel):
    """Result from semantic search"""
    chunk: KnowledgeChunk
    similarity_score: float
    relevance_explanation: Optional[str] = None


class AgentResponse(BaseModel):
    """Response from the agent"""
    query_id: str
    response_text: str
    sources: List[SearchResult] = Field(default_factory=list)
    confidence_score: float
    reasoning: Optional[str] = None
    suggested_follow_up: Optional[str] = None


class CrawlJob(BaseModel):
    """A crawling job for a knowledge source"""
    id: str
    source_type: SourceType
    source_config: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    chunks_processed: int = 0
    error_message: Optional[str] = None


class UserProfile(BaseModel):
    """User profile for personalization"""
    user_id: str
    name: str
    role: str
    team: str
    projects: List[str] = Field(default_factory=list)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    last_active: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentMetrics(BaseModel):
    """Metrics for agent performance"""
    total_queries: int
    average_response_time: float
    satisfaction_score: float
    knowledge_coverage: Dict[SourceType, float]
    top_queries: List[str]
    common_patterns: List[str]
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 