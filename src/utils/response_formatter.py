#!/usr/bin/env python3
"""
Response Formatter Utility for Agentic Mentor
Ensures consistent, well-structured AI responses
"""

import re
from typing import Dict, Any, List, Optional


class ResponseFormatter:
    """Utility class for formatting AI responses"""
    
    @staticmethod
    def format_project_response(project_name: str, content: str, metadata: Dict[str, Any]) -> str:
        """Format a project-specific response with consistent structure"""
        
        formatted_response = f"""## 📋 **{project_name}** - Project Overview

### 🎯 **Project Description**
{content}

### 🔧 **Technical Stack**
"""
        
        # Add technical details if available
        if metadata.get("language"):
            formatted_response += f"- **Primary Language:** {metadata['language']}\n"
        
        if metadata.get("technologies"):
            formatted_response += f"- **Technologies:** {metadata['technologies']}\n"
        
        if metadata.get("framework"):
            formatted_response += f"- **Framework:** {metadata['framework']}\n"
        
        if metadata.get("database"):
            formatted_response += f"- **Database:** {metadata['database']}\n"
        
        formatted_response += "\n### 🌐 **Repository Information**\n"
        
        if metadata.get("source_url"):
            formatted_response += f"- **GitHub URL:** [{project_name}]({metadata['source_url']})\n"
        
        if metadata.get("repository_name"):
            formatted_response += f"- **Repository:** {metadata['repository_name']}\n"
        
        formatted_response += "\n### 📊 **Key Features**\n"
        
        # Extract features from content
        features = ResponseFormatter._extract_features(content)
        for feature in features:
            formatted_response += f"- {feature}\n"
        
        formatted_response += "\n### 💡 **Summary**\n"
        formatted_response += ResponseFormatter._generate_summary(content)
        
        return formatted_response
    
    @staticmethod
    def format_technical_response(query: str, content: str, sources: List[Dict[str, Any]]) -> str:
        """Format a technical response with proper structure"""
        
        formatted_response = f"""## 🔍 **Query Response**

### ❓ **Your Question**
{query}

### 📚 **Information Sources**
"""
        
        for i, source in enumerate(sources, 1):
            formatted_response += f"**Source {i}:** {source.get('type', 'Unknown')}\n"
            if source.get('url'):
                formatted_response += f"**URL:** {source['url']}\n"
            formatted_response += "\n"
        
        formatted_response += "### 💡 **Detailed Answer**\n"
        formatted_response += content
        
        formatted_response += "\n### 🔗 **Related Information**\n"
        formatted_response += ResponseFormatter._generate_related_info(sources)
        
        return formatted_response
    
    @staticmethod
    def format_list_response(items: List[Dict[str, Any]], title: str) -> str:
        """Format a list response with consistent structure"""
        
        formatted_response = f"""## 📋 **{title}**

"""
        
        for i, item in enumerate(items, 1):
            formatted_response += f"### {i}. **{item.get('name', 'Unknown')}**\n"
            formatted_response += f"**Description:** {item.get('description', 'No description available')}\n"
            
            if item.get('language'):
                formatted_response += f"**Language:** {item['language']}\n"
            
            if item.get('url'):
                formatted_response += f"**URL:** [{item['name']}]({item['url']})\n"
            
            formatted_response += "\n"
        
        return formatted_response
    
    @staticmethod
    def _extract_features(content: str) -> List[str]:
        """Extract key features from content"""
        # Simple feature extraction - can be enhanced
        features = []
        
        # Look for common feature indicators
        feature_patterns = [
            r'features?[:\s]+([^.]*)',
            r'functionality[:\s]+([^.]*)',
            r'capabilities[:\s]+([^.]*)',
            r'provides?[:\s]+([^.]*)',
            r'includes?[:\s]+([^.]*)'
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if match.strip():
                    features.append(match.strip())
        
        # If no features found, create generic ones
        if not features:
            features = [
                "Comprehensive project structure",
                "Well-documented codebase",
                "Modern development practices"
            ]
        
        return features[:5]  # Limit to 5 features
    
    @staticmethod
    def _generate_summary(content: str) -> str:
        """Generate a summary of the content"""
        # Simple summary generation
        sentences = content.split('.')
        if len(sentences) > 2:
            summary = '. '.join(sentences[:2]) + '.'
        else:
            summary = content
        
        return summary
    
    @staticmethod
    def _generate_related_info(sources: List[Dict[str, Any]]) -> str:
        """Generate related information based on sources"""
        related_info = []
        
        for source in sources:
            if source.get('type') == 'github':
                related_info.append("🔗 **GitHub Repository:** Check the source code for implementation details")
            elif source.get('type') == 'documentation':
                related_info.append("📖 **Documentation:** Review the project documentation for more information")
            elif source.get('type') == 'readme':
                related_info.append("📋 **README:** Check the project README for setup and usage instructions")
        
        if not related_info:
            related_info.append("💡 **Next Steps:** Consider exploring the repository for more detailed information")
        
        return '\n'.join(related_info)
    
    @staticmethod
    def enhance_markdown_formatting(text: str) -> str:
        """Enhance markdown formatting in text"""
        
        # Ensure the text starts with a main heading if it doesn't
        if not text.strip().startswith('##'):
            text = f"## 📋 Information\n\n{text}"
        
        # Ensure proper header formatting
        text = re.sub(r'^([A-Z][^:]*):', r'### \1', text, flags=re.MULTILINE)
        
        # Enhance bullet points
        text = re.sub(r'^\* ([^:]+):', r'**\1:**', text, flags=re.MULTILINE)
        text = re.sub(r'^- ([^:]+):', r'**\1:**', text, flags=re.MULTILINE)
        
        # Add emphasis to important terms
        important_terms = ['API', 'GitHub', 'Repository', 'Project', 'Features', 'Technologies', 'Framework', 'Language', 'Database', 'Frontend', 'Backend']
        for term in important_terms:
            text = re.sub(rf'\b{term}\b', f'**{term}**', text, flags=re.IGNORECASE)
        
        # Ensure proper spacing around headers
        text = re.sub(r'\n(##[^\n]+)\n', r'\n\n\1\n\n', text)
        text = re.sub(r'\n(###[^\n]+)\n', r'\n\n\1\n\n', text)
        
        # Clean up multiple newlines
        text = re.sub(r'\n{3,}', r'\n\n', text)
        
        return text 