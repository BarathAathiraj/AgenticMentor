"""
Enhanced Crawler Agent for intelligent knowledge extraction
"""

import uuid
import re
import ast
from datetime import datetime
from typing import List, Dict, Any, Optional
from loguru import logger

from src.agents.base_agent import BaseAgent
from src.models import KnowledgeChunk, SourceType, CrawlJob
from src.knowledge.vector_store import VectorStore


class EnhancedCrawlerAgent(BaseAgent):
    """Enhanced agent for intelligent knowledge extraction from various sources"""
    
    def __init__(self, vector_store: VectorStore):
        super().__init__(
            name="Enhanced Crawler Agent",
            description="Intelligent knowledge extraction with code analysis and pattern recognition"
        )
        self.vector_store = vector_store
        self.crawlers = {
            "github_enhanced": self._create_github_enhanced_crawler(),
            "documentation": self._create_documentation_crawler(),
            "code_analysis": self._create_code_analysis_crawler(),
            "meeting_notes": self._create_meeting_notes_crawler()
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a crawl job with enhanced intelligence"""
        job_type = input_data.get("job_type", "github_enhanced")
        config = input_data.get("config", {})
        
        self._log_activity("Starting enhanced crawl", {"job_type": job_type})
        
        try:
            if job_type == "github_enhanced":
                return await self._enhanced_github_crawl(config)
            elif job_type == "documentation":
                return await self._documentation_crawl(config)
            elif job_type == "code_analysis":
                return await self._code_analysis_crawl(config)
            elif job_type == "meeting_notes":
                return await self._meeting_notes_crawl(config)
            else:
                raise ValueError(f"Unknown job type: {job_type}")
                
        except Exception as e:
            self._log_error(f"Error in enhanced crawl: {e}")
            raise
    
    async def _enhanced_github_crawl(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced GitHub crawling with code analysis"""
        from src.knowledge.crawlers import GitHubCrawler
        
        # Initialize enhanced GitHub crawler
        github_crawler = GitHubCrawler()
        
        # Get basic repository data
        basic_chunks = await github_crawler.crawl(config)
        
        # Enhanced analysis
        enhanced_chunks = []
        
        for chunk in basic_chunks:
            # Add code analysis for code files
            if "code" in chunk.metadata.get("type", ""):
                code_analysis = await self._analyze_code_content(chunk.content)
                chunk.metadata["code_analysis"] = code_analysis
            
            # Add pattern recognition
            patterns = await self._extract_patterns(chunk.content)
            chunk.metadata["patterns"] = patterns
            
            enhanced_chunks.append(chunk)
        
        # Store in vector store
        await self.vector_store.add_chunks(enhanced_chunks)
        
        self._log_activity("Enhanced GitHub crawl completed", {
            "chunks_processed": len(enhanced_chunks),
            "enhancements_added": ["code_analysis", "patterns"]
        })
        
        return {
            "job_type": "github_enhanced",
            "chunks_processed": len(enhanced_chunks),
            "enhancements": ["code_analysis", "patterns", "metadata_enhancement"]
        }
    
    async def _analyze_code_content(self, content: str) -> Dict[str, Any]:
        """Analyze code content for patterns and structure"""
        analysis = {
            "language": self._detect_language(content),
            "complexity": self._calculate_complexity(content),
            "functions": self._extract_functions(content),
            "classes": self._extract_classes(content),
            "dependencies": self._extract_dependencies(content),
            "patterns": self._detect_code_patterns(content)
        }
        return analysis
    
    def _detect_language(self, content: str) -> str:
        """Detect programming language from content"""
        # Simple language detection based on file extensions and keywords
        if "def " in content and "import " in content:
            return "python"
        elif "function " in content and "var " in content:
            return "javascript"
        elif "public class" in content or "private " in content:
            return "java"
        elif "#include" in content:
            return "cpp"
        else:
            return "unknown"
    
    def _calculate_complexity(self, content: str) -> Dict[str, Any]:
        """Calculate code complexity metrics"""
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "comment_ratio": comment_lines / total_lines if total_lines > 0 else 0
        }
    
    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions from code"""
        functions = []
        
        # Python function extraction
        if "def " in content:
            import ast
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append({
                            "name": node.name,
                            "args": [arg.arg for arg in node.args.args],
                            "line": node.lineno
                        })
            except:
                pass
        
        return functions
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions from code"""
        classes = []
        
        # Python class extraction
        if "class " in content:
            import ast
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        classes.append({
                            "name": node.name,
                            "line": node.lineno,
                            "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        })
            except:
                pass
        
        return classes
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from code"""
        dependencies = []
        
        # Python imports
        import_pattern = r'^import\s+(\w+)'
        from_pattern = r'^from\s+(\w+)'
        
        for line in content.split('\n'):
            import_match = re.search(import_pattern, line.strip())
            from_match = re.search(from_pattern, line.strip())
            
            if import_match:
                dependencies.append(import_match.group(1))
            elif from_match:
                dependencies.append(from_match.group(1))
        
        return list(set(dependencies))
    
    def _detect_code_patterns(self, content: str) -> List[str]:
        """Detect common code patterns"""
        patterns = []
        
        # Design patterns
        if "class " in content and "def __init__" in content:
            patterns.append("class_initialization")
        
        if "def " in content and "return " in content:
            patterns.append("function_with_return")
        
        if "try:" in content and "except:" in content:
            patterns.append("error_handling")
        
        if "async def" in content:
            patterns.append("async_function")
        
        if "with " in content:
            patterns.append("context_manager")
        
        return patterns
    
    async def _extract_patterns(self, content: str) -> List[str]:
        """Extract general patterns from content"""
        patterns = []
        
        # Technical patterns
        if "api" in content.lower():
            patterns.append("api_related")
        
        if "database" in content.lower() or "db" in content.lower():
            patterns.append("database_related")
        
        if "test" in content.lower():
            patterns.append("testing_related")
        
        if "config" in content.lower() or "settings" in content.lower():
            patterns.append("configuration_related")
        
        if "error" in content.lower() or "exception" in content.lower():
            patterns.append("error_handling")
        
        return patterns
    
    async def _documentation_crawl(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced documentation crawling"""
        # Implementation for documentation crawler
        return {"job_type": "documentation", "status": "not_implemented"}
    
    async def _code_analysis_crawl(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deep code analysis crawling"""
        # Implementation for code analysis crawler
        return {"job_type": "code_analysis", "status": "not_implemented"}
    
    async def _meeting_notes_crawl(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Meeting notes and calendar integration"""
        # Implementation for meeting notes crawler
        return {"job_type": "meeting_notes", "status": "not_implemented"}
    
    def _create_github_enhanced_crawler(self):
        """Create enhanced GitHub crawler"""
        return "github_enhanced"
    
    def _create_documentation_crawler(self):
        """Create documentation crawler"""
        return "documentation"
    
    def _create_code_analysis_crawler(self):
        """Create code analysis crawler"""
        return "code_analysis"
    
    def _create_meeting_notes_crawler(self):
        """Create meeting notes crawler"""
        return "meeting_notes" 