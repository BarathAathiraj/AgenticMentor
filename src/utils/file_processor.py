#!/usr/bin/env python3
"""
File Processor for Agentic Mentor
Handles document uploads and knowledge extraction from various file formats
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import PyPDF2
import docx
import markdown
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from loguru import logger
from src.knowledge.vector_store import VectorStore

class FileProcessor:
    """Process uploaded files and extract knowledge"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.supported_formats = {
            '.pdf': self._process_pdf,
            '.docx': self._process_docx,
            '.doc': self._process_doc,
            '.txt': self._process_txt,
            '.md': self._process_markdown,
            '.html': self._process_html
        }
    
    async def process_file(self, file_path: str, source_type: str = "upload") -> Dict[str, Any]:
        """Process a single file and extract knowledge"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Check if file format is supported
            file_ext = file_path.suffix.lower()
            if file_ext not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Extract text content
            content = await self.supported_formats[file_ext](file_path)
            
            # Split content into chunks
            chunks = self._split_content(content)
            
            # Add to vector store
            added_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_id = await self.vector_store.add_chunk(
                    content=chunk,
                    source_type=source_type,
                    source_url=str(file_path),
                    metadata={
                        "filename": file_path.name,
                        "file_size": file_path.stat().st_size,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                )
                added_chunks.append(chunk_id)
            
            return {
                "success": True,
                "filename": file_path.name,
                "chunks_added": len(added_chunks),
                "content_length": len(content),
                "file_size": file_path.stat().st_size
            }
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "filename": str(file_path)
            }
    
    async def process_directory(self, dir_path: str, source_type: str = "upload") -> Dict[str, Any]:
        """Process all supported files in a directory"""
        try:
            dir_path = Path(dir_path)
            if not dir_path.exists() or not dir_path.is_dir():
                raise ValueError(f"Invalid directory: {dir_path}")
            
            results = []
            total_files = 0
            successful_files = 0
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                    total_files += 1
                    result = await self.process_file(str(file_path), source_type)
                    results.append(result)
                    if result["success"]:
                        successful_files += 1
            
            return {
                "success": True,
                "total_files": total_files,
                "successful_files": successful_files,
                "failed_files": total_files - successful_files,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error processing directory {dir_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "directory": str(dir_path)
            }
    
    async def _process_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            # Try PyMuPDF first (better for complex PDFs)
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            logger.warning(f"PyMuPDF failed, trying PyPDF2: {e}")
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
    
    async def _process_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    async def _process_doc(self, file_path: Path) -> str:
        """Extract text from DOC file (requires additional libraries)"""
        # This would require python-docx or similar
        # For now, return a placeholder
        return f"DOC file processing not implemented: {file_path.name}"
    
    async def _process_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    async def _process_markdown(self, file_path: Path) -> str:
        """Extract text from Markdown file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
            # Convert markdown to HTML, then extract text
            html = markdown.markdown(md_content)
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text()
    
    async def _process_html(self, file_path: Path) -> str:
        """Extract text from HTML file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text()
    
    def _split_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into manageable chunks"""
        if len(content) <= max_chunk_size:
            return [content]
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return list(self.supported_formats.keys())
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"error": "File not found"}
            
            return {
                "filename": file_path.name,
                "file_size": file_path.stat().st_size,
                "file_type": file_path.suffix.lower(),
                "is_supported": file_path.suffix.lower() in self.supported_formats,
                "last_modified": file_path.stat().st_mtime
            }
        except Exception as e:
            return {"error": str(e)}

# Example usage
async def main():
    """Example of using the file processor"""
    processor = FileProcessor()
    
    print("📁 Agentic Mentor File Processor")
    print("=" * 40)
    print(f"Supported formats: {', '.join(processor.get_supported_formats())}")
    
    # Example: Process a sample file
    # result = await processor.process_file("sample_document.pdf", "documentation")
    # print(f"Processing result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 