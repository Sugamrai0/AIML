# AI Microservices with Flowise + LangChain

## Project Overview

This project is a comprehensive **AI microservices platform** that demonstrates modern artificial intelligence capabilities through a modular, scalable architecture. Built with Python, FastAPI, LangChain, and Flowise, it provides three specialized AI services that can be used independently or integrated into larger applications.

The platform showcases practical implementations of **Machine Learning (ML)** and **Deep Learning (DL)** fundamentals, **Retrieval-Augmented Generation (RAG)** concepts, and visual AI workflow management, making it an ideal demonstration of contemporary AI engineering practices.

## 🎯 Project Purpose & Target Audience

**Primary Purpose:**
- Demonstrate modular AI microservices architecture
- Provide reusable AI capabilities for document processing and learning assistance
- Showcase integration of multiple AI technologies in a production-ready environment
- Serve as a learning platform for AI engineering best practices

**Target Audience:**
- AI Engineers and ML Developers
- Educational Technology Platforms
- Software Developers seeking AI integration examples
- Students learning about microservices and AI orchestration
- Organizations looking to implement AI-powered document processing

## 🚀 Core Features & Capabilities

### 1. **Text Summarization Service** (Port 8001)
- **Intelligent Text Summarization**: Processes lengthy text content and generates concise, meaningful summaries
- **Document Summarization**: Supports direct file upload (PDF, DOCX, TXT) for automatic summarization
- **LLM Integration**: Leverages LangChain with open-source Large Language Models
- **Multiple Summarization Techniques**: Configurable summarization strategies for different use cases

### 2. **Q&A over Documents Service** (Port 8002)
- **Document Intelligence**: Upload and query documents using natural language questions
- **Multi-format Support**: Handles PDF, DOCX, and TXT file formats
- **RAG Implementation**: Uses Retrieval-Augmented Generation for accurate, context-aware responses
- **Vector Storage**: Integrates ChromaDB for efficient document embedding and retrieval
- **Semantic Search**: Advanced document parsing and embedding techniques for precise information extraction

### 3. **Learning Path Suggestion Service** (Port 8003)
- **Personalized Learning Recommendations**: AI-powered learning path generation based on user objectives
- **Adaptive Suggestions**: Dynamically adjusts recommendations based on user progress and preferences
- **Multiple Input Formats**: Supports both simple text input and structured JSON for complex learning scenarios
- **Educational AI**: Demonstrates practical applications of AI in education technology

### 4. **Visual AI Workflow Management** (Flowise Integration - Port 3000)
- **Visual Workflow Designer**: Drag-and-drop interface for creating AI workflows
- **LLM Orchestration**: Centralized management of language model operations
- **Multi-provider Support**: Compatible with various LLM providers (OpenRouter, Ollama, local models)
- **Workflow Persistence**: Saves and manages complex AI processing pipelines

## 🏗️ Technical Architecture

### **Microservices Architecture**
The platform follows a **distributed microservices pattern** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
├─────────────────────────────────────────────────────────────┤
│              Main API Gateway (Port 8000)                  │
├─────────────────┬─────────────────┬─────────────────────────┤
│ Text Summary    │ Q&A Documents   │ Learning Path Service   │
│ Service         │ Service         │ (Port 8003)            │
│ (Port 8001)     │ (Port 8002)     │                        │
├─────────────────┴─────────────────┴─────────────────────────┤
│              Flowise AI Orchestration Layer                │
│                    (Port 3000)                             │
├─────────────────────────────────────────────────────────────┤
│    Data Layer: ChromaDB, File Storage, Configuration       │
└─────────────────────────────────────────────────────────────┘
```

### **Service Communication**
- **API Gateway Pattern**: Central routing and request management
- **RESTful APIs**: Standard HTTP-based communication between services
- **Container Orchestration**: Docker Compose for service management
- **Persistent Storage**: Shared volumes for document uploads and vector databases

### **Key Design Patterns**
- **Separation of Concerns**: Each service handles specific AI functionality
- **Configuration as Code**: Environment-based configuration management
- **Containerization**: Docker-based deployment for consistency and scalability
- **Health Monitoring**: Built-in health check endpoints for service reliability

## 💻 Technology Stack

### **Backend Framework**
- **FastAPI**: High-performance Python web framework with automatic API documentation
- **Uvicorn**: ASGI server for production-ready async operations
- **Pydantic**: Data validation and serialization with Python type hints

### **AI & Machine Learning**
- **LangChain**: Comprehensive framework for LLM application development
- **Flowise**: Visual AI workflow builder and LLM orchestration platform
- **ChromaDB**: Vector database for document embeddings and semantic search
- **Sentence Transformers**: Advanced text embedding models

### **Document Processing**
- **PyPDF**: PDF document parsing and text extraction
- **python-docx**: Microsoft Word document processing
- **Multi-format Support**: Comprehensive document type handling

### **Development & Deployment**
- **Docker & Docker Compose**: Containerized deployment and orchestration
- **Python 3.8+**: Modern Python runtime with async support
- **Node.js**: Required for Flowise frontend and workflow management
- **Git**: Version control and collaborative development

### **Additional Libraries**
- **Requests**: HTTP client for inter-service communication
- **python-dotenv**: Environment variable management
- **aiofiles**: Asynchronous file operations
- **Jinja2**: Template engine for frontend rendering

## 📦 Deployment & Infrastructure

### **Development Environment**
- **Automated Setup**: One-command installation via `setup.py`
- **Virtual Environment**: Isolated Python environment management
- **Hot Reload**: Development-friendly auto-restart functionality
- **Local Testing**: Comprehensive test suite with `test_services.py`

### **Production Deployment**
- **Docker Containerization**: Full containerized deployment with Docker Compose
- **Service Isolation**: Independent service containers with proper networking
- **Persistent Storage**: Volume mounts for data persistence
- **Health Monitoring**: Built-in health checks and service discovery

### **Scalability Considerations**
- **Horizontal Scaling**: Individual services can be scaled independently
- **Load Balancing**: API gateway can distribute requests across service instances
- **Database Scaling**: ChromaDB can be replaced with distributed vector databases
- **Cloud Deployment**: Compatible with cloud platforms (AWS, GCP, Azure)

## 🔧 Configuration & Environment

### **Environment Variables**
- **LLM Provider Configuration**: Support for OpenRouter, Ollama, and local models
- **API Key Management**: Secure configuration for external AI services
- **Service Discovery**: Configurable service endpoints and ports
- **Database Configuration**: Flexible vector store and database settings

### **Security Features**
- **CORS Configuration**: Cross-origin request handling for web integration
- **API Key Authentication**: Secure access to external AI services
- **Environment Isolation**: Sensitive configuration through environment variables
- **File Upload Security**: Controlled document upload and processing

## 📊 Performance & Monitoring

### **Health Monitoring**
- **Service Health Checks**: Individual endpoint monitoring for each service
- **System Status**: Comprehensive health reporting across all components
- **Error Handling**: Graceful error management and reporting
- **Service Discovery**: Dynamic service status and capability reporting

### **Performance Optimization**
- **Asynchronous Operations**: Non-blocking request processing with FastAPI
- **Vector Caching**: Efficient document embedding storage and retrieval
- **Connection Pooling**: Optimized database and API connections
- **Resource Management**: Proper memory and CPU utilization

## 🎓 Educational Value & Learning Outcomes

This project serves as a comprehensive learning platform for:

### **AI/ML Concepts**
- **Large Language Model Integration**: Practical LLM application development
- **Retrieval-Augmented Generation (RAG)**: Implementation of modern AI techniques
- **Vector Databases**: Understanding of semantic search and embeddings
- **AI Workflow Design**: Visual AI pipeline creation and management

### **Software Engineering**
- **Microservices Architecture**: Distributed system design principles
- **API Design**: RESTful service development and documentation
- **Containerization**: Docker and container orchestration
- **Testing Strategies**: Comprehensive service testing approaches

### **Modern Development Practices**
- **Configuration Management**: Environment-based application configuration
- **Documentation**: Auto-generated API documentation with FastAPI
- **Version Control**: Git-based collaborative development
- **Deployment Automation**: Infrastructure as Code principles

## 🚀 Getting Started

### **Quick Start**
1. **Clone the repository**
2. **Run automated setup**: `python setup.py`
3. **Start services**: `docker-compose up --build`
4. **Access the platform**: Visit `http://localhost:8000`

### **Manual Setup**
1. **Create virtual environment**: `python -m venv venv`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure environment**: Copy `.env.example` to `.env`
4. **Start individual services** on their respective ports

## 📈 Future Enhancements & Extensibility

The platform is designed for extensibility and can be enhanced with:

- **Authentication & Authorization**: User management and access control
- **Advanced Analytics**: Usage metrics and performance monitoring
- **Additional AI Services**: Computer vision, speech processing, or other AI capabilities
- **Frontend Interface**: Complete web application for end-user interaction
- **API Rate Limiting**: Production-ready request throttling
- **Multi-language Support**: Internationalization and localization
- **Advanced Vector Stores**: Integration with enterprise vector databases
- **Workflow Templates**: Pre-built AI workflow templates for common use cases

## 🎯 Business Applications

This platform demonstrates practical AI applications for:

- **Content Management Systems**: Automated document summarization and search
- **Educational Platforms**: Personalized learning path generation
- **Knowledge Management**: Intelligent document Q&A systems
- **Research Tools**: Academic paper analysis and summarization
- **Customer Support**: AI-powered document analysis and response generation
- **Training Platforms**: Adaptive learning content recommendation

---

**This project represents a modern approach to AI microservices development, combining cutting-edge AI technologies with solid software engineering practices to create a scalable, maintainable, and educationally valuable platform.**