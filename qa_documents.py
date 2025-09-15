"""
Q&A over Documents Service
Port: 8002
"""
from fastapi import FastAPI, HTTPException
# from fastapi import UploadFile, File  # Commented out due to multipart issue
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Optional
import json
from datetime import datetime

app = FastAPI(
    title="Q&A over Documents Service",
    description="RAG-powered question answering over uploaded documents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    question: str
    answer: str
    sources: Optional[List[str]] = None

class UploadResponse(BaseModel):
    message: str
    filename: str
    status: str

# In-memory document storage for demo
documents_store = {}
# Initialize with demo document for testing
current_document = {
    "filename": "demo_ai_document.txt",
    "content": """This is a demo document about AI and machine learning technologies. 
    
Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction.
    
Machine Learning (ML) is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.
    
Flowise is a visual AI workflow builder that allows users to create complex AI applications using a drag-and-drop interface. It integrates with LangChain and various LLM providers.
    
The microservices architecture enables building scalable applications by breaking them into smaller, independent services that communicate through APIs.
    
RAG (Retrieval-Augmented Generation) systems combine the power of large language models with external knowledge bases to provide more accurate and contextual responses.""",
    "upload_time": "2024-01-01T00:00:00",
    "size": 800,
    "processed": True
}

def mock_qa_response(question: str, document_content: str, filename: str) -> str:
    """Mock Q&A response - in production, this would use RAG with vector embeddings"""
    
    # Simple keyword-based mock responses
    question_lower = question.lower()
    content_lower = document_content.lower()
    
    if any(word in question_lower for word in ['what', 'what is', 'define']):
        if 'ai' in question_lower or 'artificial intelligence' in question_lower:
            return """Based on the document content, artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. The document indicates that AI systems can perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation."""
        
        elif 'machine learning' in question_lower or 'ml' in question_lower:
            return """According to the document, machine learning is a subset of artificial intelligence that enables systems to automatically learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves."""
        
        elif 'flowise' in question_lower:
            return """The document describes Flowise as a visual AI workflow builder that allows users to create complex AI applications using a drag-and-drop interface. It integrates with LangChain and various LLM providers to build conversational AI agents and RAG applications."""
    
    elif any(word in question_lower for word in ['how', 'how to', 'explain']):
        if 'work' in question_lower:
            return """Based on the document analysis, the system works through a microservices architecture where different AI services (text summarization, document Q&A, and learning path suggestions) communicate through an API gateway. Each service integrates with Flowise for AI processing, which in turn connects to various LLM providers."""
        
        elif 'implement' in question_lower:
            return """The document outlines implementation through containerized microservices using Docker, with each service running on separate ports. The implementation uses FastAPI for the web framework, LangChain for AI orchestration, and Flowise for visual workflow management."""
    
    elif any(word in question_lower for word in ['benefits', 'advantages', 'why']):
        return """According to the document, the key benefits include: modular architecture for easy scaling, reusable AI components, visual workflow design through Flowise, support for multiple LLM providers, and simplified integration with existing applications through REST APIs."""
    
    elif 'summary' in question_lower or 'summarize' in question_lower:
        # Create a summary based on the document content
        sentences = document_content.split('. ')[:3]
        summary = '. '.join(sentences)
        return f"""Here's a summary of the key points from the document: {summary}. The document provides comprehensive information about AI microservices architecture and implementation strategies."""
    
    # Fallback response with content analysis
    word_count = len(document_content.split())
    return f"""Based on my analysis of the document "{filename}" (containing approximately {word_count} words), I can provide insights related to your question: "{question}". 

The document contains relevant information about AI/ML technologies, microservices architecture, and implementation patterns. The content suggests approaches to building scalable AI applications using modern frameworks and tools.

For more specific answers, try asking about particular topics mentioned in the document such as AI technologies, system architecture, or implementation details."""

@app.get("/")
async def root():
    return {
        "service": "Q&A over Documents Service",
        "version": "1.0.0", 
        "endpoints": ["/ask", "/health"],
        "status": "active",
        "current_document": current_document["filename"] if current_document else None
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "qa-documents"}

# Temporarily disable file upload endpoint due to multipart issue
# @app.post("/upload-document", response_model=UploadResponse)
# async def upload_document(file: UploadFile = File(...)):
#     """Upload and process document for Q&A"""
#     return UploadResponse(message="File upload temporarily disabled", filename="demo.txt", status="disabled")

@app.post("/ask", response_model=QAResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded document"""
    try:
        if not current_document:
            raise HTTPException(
                status_code=400,
                detail="No document uploaded. Please upload a document first."
            )
        
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Generate answer using mock RAG
        answer = mock_qa_response(
            request.question, 
            current_document["content"], 
            current_document["filename"]
        )
        
        return QAResponse(
            question=request.question,
            answer=answer,
            sources=[current_document["filename"]]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return {
        "documents": [
            {
                "filename": doc["filename"],
                "upload_time": doc["upload_time"],
                "size": doc["size"]
            }
            for doc in documents_store.values()
        ],
        "current_document": current_document["filename"] if current_document else None
    }

if __name__ == "__main__":
    uvicorn.run("qa_documents:app", host="0.0.0.0", port=8002, reload=True)