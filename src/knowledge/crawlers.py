"""
Crawler agents for extracting knowledge from various sources
"""

import uuid
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from loguru import logger

from src.models import KnowledgeChunk, SourceType
from src.config import settings


class BaseCrawler:
    """Base class for all crawlers"""
    
    def __init__(self, source_type: SourceType):
        self.source_type = source_type
        self.logger = logger.bind(crawler=source_type.value)
    
    async def crawl(self, config: Dict[str, Any]) -> List[KnowledgeChunk]:
        """Crawl the source and return knowledge chunks"""
        raise NotImplementedError
    
    def _create_chunk(self, 
                     content: str, 
                     source_id: str, 
                     source_url: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> KnowledgeChunk:
        """Create a knowledge chunk"""
        now = datetime.utcnow()
        return KnowledgeChunk(
            id=str(uuid.uuid4()),
            content=content,
            source_type=self.source_type,
            source_id=source_id,
            source_url=source_url,
            metadata=metadata or {},
            created_at=now,
            updated_at=now
        )
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        # Remove HTML tags if present
        content = re.sub(r'<[^>]+>', '', content)
        return content


class GitHubCrawler(BaseCrawler):
    """Crawler for GitHub repositories"""
    
    def __init__(self):
        super().__init__(SourceType.GITHUB)
        self.github_token = settings.github_token
        self.organization = settings.github_organization
        self.repos = settings.github_repos
    
    async def crawl(self, config: Dict[str, Any]) -> List[KnowledgeChunk]:
        """Crawl GitHub repositories"""
        if not self.github_token:
            self.logger.warning("GitHub token not configured")
            return []
        
        try:
            from github import Github
            
            g = Github(self.github_token)
            chunks = []
            
            # Crawl specified repositories
            repos_to_crawl = config.get('repos', self.repos)
            
            for repo_name in repos_to_crawl:
                try:
                    repo_chunks = await self._crawl_repository(g, repo_name)
                    chunks.extend(repo_chunks)
                except Exception as e:
                    self.logger.error(f"Error crawling repo {repo_name}: {e}")
            
            self.logger.info(f"Crawled {len(chunks)} chunks from GitHub")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Error in GitHub crawler: {e}")
            return []
    
    async def _crawl_repository(self, github_client, repo_name: str) -> List[KnowledgeChunk]:
        """Crawl a single repository"""
        chunks = []
        
        try:
            repo = github_client.get_repo(repo_name)
            
            # Crawl README
            if repo.description:
                chunk = self._create_chunk(
                    content=f"Repository: {repo_name}\nDescription: {repo.description}",
                    source_id=f"{repo_name}/description",
                    source_url=repo.html_url,
                    metadata={"type": "description", "language": repo.language}
                )
                chunks.append(chunk)
            
            # Crawl README file
            try:
                readme = repo.get_readme()
                content = readme.decoded_content.decode('utf-8')
                chunk = self._create_chunk(
                    content=self._clean_content(content),
                    source_id=f"{repo_name}/readme",
                    source_url=f"{repo.html_url}/blob/main/README.md",
                    metadata={"type": "readme", "language": repo.language}
                )
                chunks.append(chunk)
            except Exception as e:
                self.logger.debug(f"No README found for {repo_name}: {e}")
            
            # Crawl issues
            issues = repo.get_issues(state='all', sort='updated', direction='desc')
            for issue in list(issues)[:50]:  # Limit to recent issues
                content = f"Issue #{issue.number}: {issue.title}\n\n{issue.body or ''}"
                chunk = self._create_chunk(
                    content=self._clean_content(content),
                    source_id=f"{repo_name}/issue/{issue.number}",
                    source_url=issue.html_url,
                    metadata={
                        "type": "issue",
                        "state": issue.state,
                        "labels": [label.name for label in issue.labels],
                        "created_at": issue.created_at.isoformat()
                    }
                )
                chunks.append(chunk)
            
            # Crawl pull requests
            prs = repo.get_pulls(state='all', sort='updated', direction='desc')
            for pr in list(prs)[:30]:  # Limit to recent PRs
                content = f"PR #{pr.number}: {pr.title}\n\n{pr.body or ''}"
                chunk = self._create_chunk(
                    content=self._clean_content(content),
                    source_id=f"{repo_name}/pr/{pr.number}",
                    source_url=pr.html_url,
                    metadata={
                        "type": "pull_request",
                        "state": pr.state,
                        "created_at": pr.created_at.isoformat()
                    }
                )
                chunks.append(chunk)
            
        except Exception as e:
            self.logger.error(f"Error crawling repository {repo_name}: {e}")
        
        return chunks


class JiraCrawler(BaseCrawler):
    """Crawler for Jira issues"""
    
    def __init__(self):
        super().__init__(SourceType.JIRA)
        self.server = settings.jira_server
        self.username = settings.jira_username
        self.api_token = settings.jira_api_token
        self.projects = settings.jira_projects
    
    async def crawl(self, config: Dict[str, Any]) -> List[KnowledgeChunk]:
        """Crawl Jira issues"""
        if not all([self.server, self.username, self.api_token]):
            self.logger.warning("Jira credentials not fully configured")
            return []
        
        try:
            from jira import JIRA
            
            jira = JIRA(
                server=self.server,
                basic_auth=(self.username, self.api_token)
            )
            
            chunks = []
            projects_to_crawl = config.get('projects', self.projects)
            
            for project_key in projects_to_crawl:
                try:
                    project_chunks = await self._crawl_project(jira, project_key)
                    chunks.extend(project_chunks)
                except Exception as e:
                    self.logger.error(f"Error crawling Jira project {project_key}: {e}")
            
            self.logger.info(f"Crawled {len(chunks)} chunks from Jira")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Error in Jira crawler: {e}")
            return []
    
    async def _crawl_project(self, jira_client, project_key: str) -> List[KnowledgeChunk]:
        """Crawl issues from a Jira project"""
        chunks = []
        
        try:
            # Get project info
            project = jira_client.project(project_key)
            
            # Search for issues
            jql = f"project = {project_key} ORDER BY updated DESC"
            issues = jira_client.search_issues(jql, maxResults=100)
            
            for issue in issues:
                # Create content from issue
                content_parts = [
                    f"Issue: {issue.key}",
                    f"Summary: {issue.fields.summary}",
                    f"Description: {issue.fields.description or 'No description'}"
                ]
                
                # Add comments
                if hasattr(issue.fields, 'comment') and issue.fields.comment.comments:
                    content_parts.append("Comments:")
                    for comment in issue.fields.comment.comments:
                        content_parts.append(f"- {comment.author.displayName}: {comment.body}")
                
                content = "\n\n".join(content_parts)
                
                chunk = self._create_chunk(
                    content=self._clean_content(content),
                    source_id=issue.key,
                    source_url=f"{self.server}/browse/{issue.key}",
                    metadata={
                        "type": "issue",
                        "status": issue.fields.status.name,
                        "priority": issue.fields.priority.name if issue.fields.priority else None,
                        "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                        "created_at": issue.fields.created,
                        "updated_at": issue.fields.updated
                    }
                )
                chunks.append(chunk)
        
        except Exception as e:
            self.logger.error(f"Error crawling Jira project {project_key}: {e}")
        
        return chunks


class ConfluenceCrawler(BaseCrawler):
    """Crawler for Confluence pages"""
    
    def __init__(self):
        super().__init__(SourceType.CONFLUENCE)
        self.server = settings.confluence_server
        self.username = settings.confluence_username
        self.api_token = settings.confluence_api_token
        self.spaces = settings.confluence_space_keys
    
    async def crawl(self, config: Dict[str, Any]) -> List[KnowledgeChunk]:
        """Crawl Confluence pages"""
        if not all([self.server, self.username, self.api_token]):
            self.logger.warning("Confluence credentials not fully configured")
            return []
        
        try:
            from atlassian import Confluence
            
            confluence = Confluence(
                url=self.server,
                username=self.username,
                password=self.api_token,
                cloud=True
            )
            
            chunks = []
            spaces_to_crawl = config.get('spaces', self.spaces)
            
            for space_key in spaces_to_crawl:
                try:
                    space_chunks = await self._crawl_space(confluence, space_key)
                    chunks.extend(space_chunks)
                except Exception as e:
                    self.logger.error(f"Error crawling Confluence space {space_key}: {e}")
            
            self.logger.info(f"Crawled {len(chunks)} chunks from Confluence")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Error in Confluence crawler: {e}")
            return []
    
    async def _crawl_space(self, confluence_client, space_key: str) -> List[KnowledgeChunk]:
        """Crawl pages from a Confluence space"""
        chunks = []
        
        try:
            # Get space info
            space = confluence_client.get_space(space_key)
            
            # Get pages in the space
            pages = confluence_client.get_all_pages_from_space(space_key, start=0, limit=100)
            
            for page in pages:
                try:
                    # Get page content
                    page_content = confluence_client.get_page_by_id(page['id'], expand='body.storage')
                    
                    content = f"Page: {page_content['title']}\n\n{page_content['body']['storage']['value']}"
                    
                    chunk = self._create_chunk(
                        content=self._clean_content(content),
                        source_id=page_content['id'],
                        source_url=f"{self.server}/wiki{page_content['_links']['webui']}",
                        metadata={
                            "type": "page",
                            "space_key": space_key,
                            "created_at": page_content['created'],
                            "updated_at": page_content['version']['when']
                        }
                    )
                    chunks.append(chunk)
                
                except Exception as e:
                    self.logger.debug(f"Error processing Confluence page {page.get('id')}: {e}")
        
        except Exception as e:
            self.logger.error(f"Error crawling Confluence space {space_key}: {e}")
        
        return chunks


class SlackCrawler(BaseCrawler):
    """Crawler for Slack messages"""
    
    def __init__(self):
        super().__init__(SourceType.SLACK)
        self.bot_token = settings.slack_bot_token
        self.app_token = settings.slack_app_token
        self.channels = settings.slack_channels
    
    async def crawl(self, config: Dict[str, Any]) -> List[KnowledgeChunk]:
        """Crawl Slack messages"""
        if not all([self.bot_token, self.app_token]):
            self.logger.warning("Slack credentials not fully configured")
            return []
        
        try:
            from slack_sdk.web import WebClient
            from slack_sdk.socket_mode import SocketModeClient
            
            client = WebClient(token=self.bot_token)
            chunks = []
            channels_to_crawl = config.get('channels', self.channels)
            
            for channel_name in channels_to_crawl:
                try:
                    channel_chunks = await self._crawl_channel(client, channel_name)
                    chunks.extend(channel_chunks)
                except Exception as e:
                    self.logger.error(f"Error crawling Slack channel {channel_name}: {e}")
            
            self.logger.info(f"Crawled {len(chunks)} chunks from Slack")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Error in Slack crawler: {e}")
            return []
    
    async def _crawl_channel(self, slack_client, channel_name: str) -> List[KnowledgeChunk]:
        """Crawl messages from a Slack channel"""
        chunks = []
        
        try:
            # Get channel info
            channel_info = slack_client.conversations_list()
            channel_id = None
            
            for channel in channel_info['channels']:
                if channel['name'] == channel_name:
                    channel_id = channel['id']
                    break
            
            if not channel_id:
                self.logger.warning(f"Channel {channel_name} not found")
                return chunks
            
            # Get messages from channel
            messages = slack_client.conversations_history(
                channel=channel_id,
                limit=100
            )
            
            for message in messages['messages']:
                # Skip bot messages and system messages
                if message.get('bot_id') or message.get('subtype'):
                    continue
                
                content = f"Channel: #{channel_name}\nUser: {message.get('user', 'Unknown')}\nMessage: {message.get('text', '')}"
                
                chunk = self._create_chunk(
                    content=self._clean_content(content),
                    source_id=message['ts'],
                    source_url=f"https://slack.com/app_redirect?channel={channel_id}&message_ts={message['ts']}",
                    metadata={
                        "type": "message",
                        "channel": channel_name,
                        "user": message.get('user'),
                        "timestamp": message['ts']
                    }
                )
                chunks.append(chunk)
        
        except Exception as e:
            self.logger.error(f"Error crawling Slack channel {channel_name}: {e}")
        
        return chunks 