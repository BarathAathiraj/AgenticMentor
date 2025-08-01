"""
Vector store for knowledge chunks
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from loguru import logger

from src.models import KnowledgeChunk, SourceType
from src.config import settings


class VectorStore:
    """Vector store for storing and retrieving knowledge chunks"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection("knowledge_chunks")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.logger = logger.bind(component="vector_store")
        
    async def add_chunk(self, chunk: KnowledgeChunk) -> str:
        """Add a knowledge chunk to the vector store"""
        try:
            # Generate embedding
            embedding = self.embedding_model.encode(chunk.content).tolist()
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk.content],
                metadatas=[{
                    "id": chunk.id,
                    "source_type": chunk.source_type.value,
                    "source_id": chunk.source_id,
                    "source_url": chunk.source_url or "",
                    "created_at": chunk.created_at.isoformat(),
                    "updated_at": chunk.updated_at.isoformat(),
                    **chunk.metadata
                }],
                ids=[chunk.id]
            )
            
            self.logger.info(f"Added chunk {chunk.id} to vector store")
            return chunk.id
            
        except Exception as e:
            self.logger.error(f"Error adding chunk to vector store: {e}")
            raise
    
    async def add_chunks(self, chunks: List[KnowledgeChunk]) -> List[str]:
        """Add multiple knowledge chunks to the vector store"""
        if not chunks:
            return []
        
        try:
            # Generate embeddings
            contents = [chunk.content for chunk in chunks]
            embeddings = self.embedding_model.encode(contents).tolist()
            
            # Prepare metadata
            metadatas = []
            ids = []
            
            for chunk in chunks:
                metadatas.append({
                    "id": chunk.id,
                    "source_type": chunk.source_type.value,
                    "source_id": chunk.source_id,
                    "source_url": chunk.source_url or "",
                    "created_at": chunk.created_at.isoformat(),
                    "updated_at": chunk.updated_at.isoformat(),
                    **chunk.metadata
                })
                ids.append(chunk.id)
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=contents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Added {len(chunks)} chunks to vector store")
            return ids
            
        except Exception as e:
            self.logger.error(f"Error adding chunks to vector store: {e}")
            raise
    
    async def search(self, 
                    query: str, 
                    limit: int = 10,
                    source_types: Optional[List[SourceType]] = None,
                    filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar chunks"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause
            where = {}
            if source_types:
                where["source_type"] = {"$in": [st.value for st in source_types]}
            if filters:
                where.update(filters)
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where if where else None
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                chunk = KnowledgeChunk(
                    id=results['ids'][0][i],
                    content=results['documents'][0][i],
                    source_type=SourceType(results['metadatas'][0][i]['source_type']),
                    source_id=results['metadatas'][0][i]['source_id'],
                    source_url=results['metadatas'][0][i].get('source_url'),
                    metadata={k: v for k, v in results['metadatas'][0][i].items() 
                             if k not in ['id', 'source_type', 'source_id', 'source_url', 'created_at', 'updated_at']},
                    created_at=datetime.fromisoformat(results['metadatas'][0][i]['created_at']),
                    updated_at=datetime.fromisoformat(results['metadatas'][0][i]['updated_at'])
                )
                
                formatted_results.append({
                    "chunk": chunk,
                    "similarity_score": 1 - results['distances'][0][i]  # Convert distance to similarity
                })
            
            self.logger.info(f"Search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error searching vector store: {e}")
            raise
    
    async def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk from the vector store"""
        try:
            self.collection.delete(ids=[chunk_id])
            self.logger.info(f"Deleted chunk {chunk_id} from vector store")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting chunk from vector store: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            count = self.collection.count()
            
            # Get source type distribution
            results = self.collection.get(include=['metadatas'])
            source_types = {}
            for metadata in results['metadatas']:
                source_type = metadata['source_type']
                source_types[source_type] = source_types.get(source_type, 0) + 1
            
            return {
                "total_chunks": count,
                "source_type_distribution": source_types
            }
        except Exception as e:
            self.logger.error(f"Error getting vector store stats: {e}")
            return {"total_chunks": 0, "source_type_distribution": {}}
    
    async def clear(self) -> bool:
        """Clear all chunks from the vector store"""
        try:
            self.collection.delete(where={})
            self.logger.info("Cleared all chunks from vector store")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing vector store: {e}")
            return False 