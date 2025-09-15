"""
Main entry point for AI Microservices with Flowise + LangChain
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="AI Microservices with Flowise + LangChain",
    description="API for text summarization, Q&A over documents, and dynamic learning path suggestion",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     """Serve the main website"""
#     return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
async def api_root():
    return {
        "message": "AI Microservices with Flowise + LangChain API",
        "services": [
            "text-summarization",
            "qa-documents", 
            "learning-path"
        ],
        "docs": "/docs",
        "website": "/"
    }

@app.get("/api/services")
async def get_services():
    """Get service status and endpoints"""
    return {
        "services": {
            "text_summarization": {
                "name": "Text Summarization Service",
                "port": 8001,
                "endpoints": [
                    "/summarize",
                    "/summarize-document"
                ],
                "status": "active"
            },
            "qa_documents": {
                "name": "Q&A over Documents Service", 
                "port": 8002,
                "endpoints": [
                    "/upload-document",
                    "/ask"
                ],
                "status": "active"
            },
            "learning_path": {
                "name": "Learning Path Suggestion Service",
                "port": 8003,
                "endpoints": [
                    "/suggest-path",
                    "/suggest-path-json"
                ],
                "status": "active"
            },
            "flowise": {
                "name": "Flowise AI Orchestration",
                "port": 3000,
                "description": "Visual AI workflow builder",
                "status": "active"
            }
        }
    }

@app.get("/api/health")
async def health_check():
    """Enhanced health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "main_api": "running",
            "static_files": "mounted", 
            "templates": "configured"
        },
        "features": [
            "AI Microservices",
            "Flowise Integration",
            "SSO Authentication Demo",
            "Interactive API Documentation"
        ]
    }

# Legacy health endpoint for backward compatibility
@app.get("/health")
async def legacy_health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {
        "message": "AI Microservices with Flowise + LangChain",
        "services": [
            "text-summarization",
            "qa-documents", 
            "learning-path"
        ],
        "docs": "/docs",
        "api": "/api",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)