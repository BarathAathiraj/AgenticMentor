"""
Configuration management for Agentic Mentor
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # LLM Configuration
    openai_api_key: Optional[str] = Field("demo_key", env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo-preview", env="OPENAI_MODEL")
    
    # Gemini Configuration
    use_gemini: bool = Field(False, env="USE_GEMINI")
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    
    # Grok Configuration
    use_grok: bool = Field(False, env="USE_GROK")
    grok_api_key: Optional[str] = Field(None, env="GROK_API_KEY")
    grok_model: str = Field("grok-beta", env="GROK_MODEL")
    
    # Vector Store Configuration
    vector_store_type: str = Field("chroma", env="VECTOR_STORE_TYPE")
    chroma_persist_directory: str = Field("./data/chroma", env="CHROMA_PERSIST_DIRECTORY")
    pinecone_api_key: Optional[str] = Field(None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(None, env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field("agentic-mentor", env="PINECONE_INDEX_NAME")
    
    # Database Configuration
    database_url: str = Field("sqlite:///./data/agentic_mentor.db", env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # GitHub Integration
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    github_organization: Optional[str] = Field(None, env="GITHUB_ORGANIZATION")
    github_repos: List[str] = Field(default_factory=list, env="GITHUB_REPOS")
    
    # Jira Integration
    jira_server: Optional[str] = Field(None, env="JIRA_SERVER")
    jira_username: Optional[str] = Field(None, env="JIRA_USERNAME")
    jira_api_token: Optional[str] = Field(None, env="JIRA_API_TOKEN")
    jira_projects: List[str] = Field(default_factory=list, env="JIRA_PROJECTS")
    
    # Confluence Integration
    confluence_server: Optional[str] = Field(None, env="CONFLUENCE_SERVER")
    confluence_username: Optional[str] = Field(None, env="CONFLUENCE_USERNAME")
    confluence_api_token: Optional[str] = Field(None, env="CONFLUENCE_API_TOKEN")
    confluence_space_keys: List[str] = Field(default_factory=list, env="CONFLUENCE_SPACE_KEYS")
    
    # Slack Integration
    slack_bot_token: Optional[str] = Field(None, env="SLACK_BOT_TOKEN")
    slack_app_token: Optional[str] = Field(None, env="SLACK_APP_TOKEN")
    slack_channels: List[str] = Field(default_factory=list, env="SLACK_CHANNELS")
    
    # Web Server Configuration
    web_host: str = Field("0.0.0.0", env="WEB_HOST")
    web_port: int = Field(8000, env="WEB_PORT")
    web_debug: bool = Field(False, env="WEB_DEBUG")
    
    # Security Configuration
    secret_key: str = Field("demo-secret-key", env="SECRET_KEY")
    encryption_key: str = Field("demo-encryption-key", env="ENCRYPTION_KEY")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("./logs/agentic_mentor.log", env="LOG_FILE")
    
    # Agent Configuration
    agent_memory_size: int = Field(1000, env="AGENT_MEMORY_SIZE")
    agent_reflection_enabled: bool = Field(True, env="AGENT_REFLECTION_ENABLED")
    agent_learning_rate: float = Field(0.1, env="AGENT_LEARNING_RATE")
    
    # Search Configuration
    search_max_results: int = Field(10, env="SEARCH_MAX_RESULTS")
    search_similarity_threshold: float = Field(0.7, env="SEARCH_SIMILARITY_THRESHOLD")
    
    # Crawler Configuration
    crawler_max_depth: int = Field(3, env="CRAWLER_MAX_DEPTH")
    crawler_delay: float = Field(1.0, env="CRAWLER_DELAY")
    crawler_timeout: int = Field(30, env="CRAWLER_TIMEOUT")
    
    # Rate Limiting
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(3600, env="RATE_LIMIT_WINDOW")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings() 