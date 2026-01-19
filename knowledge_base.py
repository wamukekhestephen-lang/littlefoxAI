"""
Knowledge Base Management System
Handles document ingestion, embedding, and retrieval
"""

import os
import json
from pathlib import Path
import PyPDF2
from docx import Document
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class KnowledgeBase:
    def __init__(self, kb_dir="knowledge_base"):
        self.kb_dir = kb_dir
        self.embeddings_file = os.path.join(kb_dir, "embeddings.json")
        self.documents_file = os.path.join(kb_dir, "documents.json")
        self.metadata_file = os.path.join(kb_dir, "metadata.json")
        
        # Create directory if it doesn't exist
        os.makedirs(kb_dir, exist_ok=True)
        
        self.embeddings = {}
        self.documents = {}
        self.metadata = {}
        
        self.load()
    
    def load(self):
        """Load existing knowledge base"""
        if os.path.exists(self.embeddings_file):
            with open(self.embeddings_file, 'r') as f:
                self.embeddings = json.load(f)
        
        if os.path.exists(self.documents_file):
            with open(self.documents_file, 'r') as f:
                self.documents = json.load(f)
        
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
    
    def save(self):
        """Save knowledge base to disk"""
        with open(self.embeddings_file, 'w') as f:
            json.dump(self.embeddings, f)
        
        with open(self.documents_file, 'w') as f:
            json.dump(self.documents, f)
        
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)
    
    def extract_text_from_pdf(self, filepath):
        """Extract text from PDF"""
        try:
            text = ""
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, filepath):
        """Extract text from Word document"""
        try:
            doc = Document(filepath)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, filepath):
        """Extract text from text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    
    def ingest_document(self, filepath, doc_name=None):
        """Ingest a document and create embeddings"""
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return False
        
        doc_name = doc_name or os.path.basename(filepath)
        
        # Extract text based on file type
        ext = Path(filepath).suffix.lower()
        if ext == '.pdf':
            text = self.extract_text_from_pdf(filepath)
        elif ext == '.docx':
            text = self.extract_text_from_docx(filepath)
        elif ext == '.txt':
            text = self.extract_text_from_txt(filepath)
        else:
            print(f"Unsupported file type: {ext}")
            return False
        
        if not text:
            print("No text extracted from document")
            return False
        
        # Split into chunks
        chunks = self.split_into_chunks(text, chunk_size=1000)
        
        # Create embeddings for each chunk
        for i, chunk in enumerate(chunks):
            try:
                response = client.embeddings.create(
                    input=chunk,
                    model="text-embedding-3-small"
                )
                embedding = response.data[0].embedding
                
                chunk_id = f"{doc_name}_{i}"
                self.embeddings[chunk_id] = embedding
                self.documents[chunk_id] = chunk
                
                if doc_name not in self.metadata:
                    self.metadata[doc_name] = {
                        "chunks": 0,
                        "ingested_at": str(Path(filepath).stat().st_mtime),
                        "filepath": filepath
                    }
                
                self.metadata[doc_name]["chunks"] += 1
                
                print(f"  ✓ Chunk {i+1}/{len(chunks)} embedded")
            except Exception as e:
                print(f"Error creating embedding: {e}")
                return False
        
        self.save()
        print(f"✓ Document '{doc_name}' ingested successfully ({len(chunks)} chunks)")
        return True
    
    def split_into_chunks(self, text, chunk_size=1000, overlap=100):
        """Split text into overlapping chunks"""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks
    
    def search(self, query, top_k=3):
        """Search knowledge base for relevant documents"""
        if not self.embeddings:
            return []
        
        try:
            # Get embedding for query
            response = client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            query_embedding = response.data[0].embedding
            
            # Calculate similarity scores
            scores = {}
            for chunk_id, embedding in self.embeddings.items():
                similarity = np.dot(query_embedding, embedding)
                scores[chunk_id] = similarity
            
            # Get top K results
            top_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
            
            results = []
            for chunk_id, score in top_results:
                results.append({
                    "id": chunk_id,
                    "text": self.documents[chunk_id],
                    "score": float(score)
                })
            
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def list_documents(self):
        """List all ingested documents"""
        return self.metadata
    
    def add_custom_knowledge(self, category, key, value):
        """Add custom knowledge (rules, examples, domain-specific info)"""
        if "custom_knowledge" not in self.metadata:
            self.metadata["custom_knowledge"] = {}
        
        if category not in self.metadata["custom_knowledge"]:
            self.metadata["custom_knowledge"][category] = {}
        
        self.metadata["custom_knowledge"][category][key] = value
        self.save()
        print(f"✓ Added custom knowledge: {category}/{key}")
    
    def get_custom_knowledge(self, category=None):
        """Retrieve custom knowledge"""
        custom = self.metadata.get("custom_knowledge", {})
        if category:
            return custom.get(category, {})
        return custom


# Create global instance
kb = KnowledgeBase()
