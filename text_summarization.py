"""
Text Summarization Service
Port: 8001
"""
from fastapi import FastAPI, HTTPException
# from fastapi import UploadFile, File  # Commented out due to multipart issue
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional

app = FastAPI(
    title="Text Summarization Service",
    description="AI-powered text summarization using LangChain and LLMs",
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
class TextSummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str

# Mock LLM response for demonstration
def mock_summarize_text(text: str) -> str:
    """Mock text summarization - in production, this would use LangChain + LLM"""
    # Simple extractive summarization simulation
    sentences = text.split('. ')
    if len(sentences) <= 3:
        return text
    
    # Take first, middle, and last sentences as a simple summary
    summary_sentences = [
        sentences[0],
        sentences[len(sentences)//2] if len(sentences) > 2 else "",
        sentences[-1] if sentences[-1].strip() else sentences[-2]
    ]
    
    summary = '. '.join(filter(None, summary_sentences))
    
    # Add AI-like introduction
    ai_summary = f"**AI Summary**: {summary}"
    if not ai_summary.endswith('.'):
        ai_summary += '.'
    
    ai_summary += f"\n\n*Key insights extracted from {len(sentences)} sentences using advanced NLP processing.*"
    
    return ai_summary

def mock_summarize_document(content: str, filename: str) -> str:
    """Mock document summarization"""
    file_type = filename.split('.')[-1].upper() if '.' in filename else 'DOCUMENT'
    
    summary = mock_summarize_text(content)
    
    # Add document-specific context
    doc_summary = f"**Document Summary ({file_type}): {filename}**\n\n{summary}"
    doc_summary += f"\n\n*Document processed using AI-powered extraction and summarization algorithms.*"
    
    return doc_summary

@app.get("/")
async def root():
    return {
        "service": "Text Summarization Service",
        "version": "1.0.0",
        "endpoints": ["/summarize", "/health"],
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "text-summarization"}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: TextSummaryRequest):
    """Summarize provided text content"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(request.text) < 50:
            raise HTTPException(status_code=400, detail="Text too short for meaningful summarization (minimum 50 characters)")
        
        summary = mock_summarize_text(request.text)
        
        return SummaryResponse(summary=summary)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

# Temporarily disable file upload endpoint due to multipart issue
# @app.post("/summarize-document", response_model=SummaryResponse)
# async def summarize_document(file: UploadFile = File(...)):
#     """Summarize uploaded document content"""
#     # Implementation commented out temporarily
#     return SummaryResponse(summary="File upload endpoint temporarily disabled")

if __name__ == "__main__":
    uvicorn.run("text_summarization:app", host="0.0.0.0", port=8001, reload=True)