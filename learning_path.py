"""
Learning Path Suggestion Service
Port: 8003
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional, List, Dict
import json

app = FastAPI(
    title="Learning Path Suggestion Service",
    description="AI-powered personalized learning path recommendations",
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
class LearningPathRequest(BaseModel):
    text: str

class LearningPathJSONRequest(BaseModel):
    goals: str
    experience_level: Optional[str] = "beginner"
    time_commitment: Optional[str] = "3-5 hours/week"
    preferred_learning_style: Optional[str] = "mixed"

class LearningPhase(BaseModel):
    title: str
    description: str
    duration: str
    resources: List[str]
    skills_gained: List[str]

class LearningPathResponse(BaseModel):
    learning_path: str
    phases: Optional[List[LearningPhase]] = None
    total_duration: Optional[str] = None
    difficulty: Optional[str] = None

def generate_learning_path(goals: str, experience_level: str = "beginner", time_commitment: str = "3-5 hours/week") -> Dict:
    """Generate a comprehensive learning path based on user input"""
    
    # Determine focus areas from goals
    goals_lower = goals.lower()
    focus_areas = []
    
    if any(term in goals_lower for term in ['machine learning', 'ml', 'ai', 'artificial intelligence']):
        focus_areas.append('machine_learning')
    if any(term in goals_lower for term in ['deep learning', 'neural networks', 'dl']):
        focus_areas.append('deep_learning')
    if any(term in goals_lower for term in ['python', 'programming', 'code']):
        focus_areas.append('programming')
    if any(term in goals_lower for term in ['data science', 'data analysis', 'data']):
        focus_areas.append('data_science')
    if any(term in goals_lower for term in ['web', 'api', 'backend']):
        focus_areas.append('web_development')
    if any(term in goals_lower for term in ['flowise', 'langchain', 'llm']):
        focus_areas.append('ai_frameworks')
    
    # Default to ML if no specific focus detected
    if not focus_areas:
        focus_areas = ['machine_learning']
    
    # Generate phases based on experience level and focus areas
    phases = []
    
    if experience_level == "beginner":
        # Foundation phase
        phases.append(LearningPhase(
            title="Foundation & Prerequisites",
            description="Build essential mathematical and programming foundations for AI/ML",
            duration="4-6 weeks",
            resources=[
                "Python Programming Fundamentals",
                "Linear Algebra for ML (Khan Academy)",
                "Statistics and Probability Basics",
                "Pandas and NumPy tutorials"
            ],
            skills_gained=["Python programming", "Basic mathematics", "Data manipulation"]
        ))
        
        # Core ML phase
        if 'machine_learning' in focus_areas:
            phases.append(LearningPhase(
                title="Machine Learning Fundamentals",
                description="Learn core ML concepts, algorithms, and practical implementation",
                duration="6-8 weeks",
                resources=[
                    "Andrew Ng's Machine Learning Course",
                    "Scikit-learn documentation and tutorials",
                    "Hands-on ML projects with real datasets",
                    "Kaggle Learn ML courses"
                ],
                skills_gained=["Supervised/Unsupervised learning", "Model evaluation", "Feature engineering"]
            ))
        
        if 'deep_learning' in focus_areas:
            phases.append(LearningPhase(
                title="Deep Learning & Neural Networks",
                description="Dive into neural networks, deep learning frameworks, and advanced AI",
                duration="8-10 weeks",
                resources=[
                    "Deep Learning Specialization (Coursera)",
                    "TensorFlow and PyTorch tutorials",
                    "CNN and RNN implementation projects",
                    "Computer Vision and NLP applications"
                ],
                skills_gained=["Neural network design", "Deep learning frameworks", "AI applications"]
            ))
        
        if 'ai_frameworks' in focus_areas:
            phases.append(LearningPhase(
                title="Modern AI Frameworks & Tools",
                description="Master LangChain, Flowise, and production AI development",
                duration="4-6 weeks",
                resources=[
                    "LangChain documentation and examples",
                    "Flowise tutorial series",
                    "Building RAG applications",
                    "LLM integration best practices"
                ],
                skills_gained=["LangChain development", "AI workflow design", "Production deployment"]
            ))
    
    elif experience_level == "intermediate":
        phases.append(LearningPhase(
            title="Advanced ML Techniques",
            description="Explore advanced algorithms, ensemble methods, and optimization",
            duration="4-5 weeks",
            resources=[
                "Advanced Scikit-learn techniques",
                "XGBoost and LightGBM mastery", 
                "Hyperparameter optimization",
                "MLOps fundamentals"
            ],
            skills_gained=["Advanced algorithms", "Model optimization", "Production workflows"]
        ))
        
        if 'ai_frameworks' in focus_areas:
            phases.append(LearningPhase(
                title="AI Application Development",
                description="Build production-ready AI applications with modern frameworks",
                duration="6-8 weeks",
                resources=[
                    "Advanced LangChain patterns",
                    "Flowise custom component development",
                    "Vector databases and embeddings",
                    "API design for AI services"
                ],
                skills_gained=["Advanced AI development", "System architecture", "Production deployment"]
            ))
    
    # Add a project phase
    phases.append(LearningPhase(
        title="Capstone Project",
        description="Apply your skills in a comprehensive, portfolio-worthy project",
        duration="3-4 weeks",
        resources=[
            "Choose a real-world problem to solve",
            "Implement end-to-end solution",
            "Deploy to cloud platform",
            "Document and present your work"
        ],
        skills_gained=["Project management", "Full-stack AI development", "Portfolio development"]
    ))
    
    # Calculate total duration
    total_weeks = sum(int(phase.duration.split('-')[0]) for phase in phases)
    total_duration = f"{total_weeks}-{total_weeks + len(phases)} weeks"
    
    # Generate descriptive text
    learning_path_text = f"""
## Personalized Learning Path: {', '.join(focus_areas).replace('_', ' ').title()}

### Overview
Based on your goals and {experience_level} experience level, this learning path is designed for {time_commitment} commitment and will take approximately {total_duration} to complete.

### Learning Journey
"""
    
    for i, phase in enumerate(phases, 1):
        learning_path_text += f"""
**Phase {i}: {phase.title}** ({phase.duration})
{phase.description}

Key Skills: {', '.join(phase.skills_gained)}
"""
    
    learning_path_text += f"""
### Success Tips
- Follow the phases in order for optimal learning progression
- Practice with real projects alongside theoretical learning
- Join AI/ML communities for support and networking
- Build a portfolio showcasing your projects
- Stay updated with latest AI developments and tools

### Next Steps After Completion
- Advanced specialization in your area of interest
- Contribute to open-source AI projects
- Consider AI/ML certifications
- Build and deploy your own AI applications
"""
    
    return {
        "learning_path": learning_path_text,
        "phases": phases,
        "total_duration": total_duration,
        "difficulty": experience_level,
        "focus_areas": focus_areas
    }

@app.get("/")
async def root():
    return {
        "service": "Learning Path Suggestion Service",
        "version": "1.0.0",
        "endpoints": ["/suggest-path", "/suggest-path-json", "/health"],
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "learning-path"}

@app.post("/suggest-path", response_model=LearningPathResponse)
async def suggest_learning_path(request: LearningPathRequest):
    """Generate learning path from text description"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Learning goals cannot be empty")
        
        # Generate learning path with default parameters
        path_data = generate_learning_path(
            goals=request.text,
            experience_level="beginner",
            time_commitment="3-5 hours/week"
        )
        
        return LearningPathResponse(
            learning_path=path_data["learning_path"],
            phases=path_data["phases"],
            total_duration=path_data["total_duration"],
            difficulty=path_data["difficulty"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")

@app.post("/suggest-path-json", response_model=LearningPathResponse)
async def suggest_learning_path_json(request: LearningPathJSONRequest):
    """Generate learning path from structured JSON input"""
    try:
        if not request.goals.strip():
            raise HTTPException(status_code=400, detail="Learning goals cannot be empty")
        
        # Generate learning path with provided parameters
        path_data = generate_learning_path(
            goals=request.goals,
            experience_level=request.experience_level,
            time_commitment=request.time_commitment
        )
        
        return LearningPathResponse(
            learning_path=path_data["learning_path"],
            phases=path_data["phases"],
            total_duration=path_data["total_duration"],
            difficulty=path_data["difficulty"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")

@app.get("/templates")
async def get_learning_templates():
    """Get predefined learning path templates"""
    return {
        "templates": [
            {
                "name": "ML Engineer Path",
                "description": "Comprehensive path to become a Machine Learning Engineer",
                "duration": "16-20 weeks",
                "focus": ["machine_learning", "programming", "mlops"]
            },
            {
                "name": "AI Application Developer",
                "description": "Build AI-powered applications with modern frameworks",
                "duration": "12-16 weeks", 
                "focus": ["ai_frameworks", "web_development", "programming"]
            },
            {
                "name": "Data Scientist Path",
                "description": "Master data science and machine learning",
                "duration": "18-22 weeks",
                "focus": ["data_science", "machine_learning", "programming"]
            },
            {
                "name": "Deep Learning Specialist",
                "description": "Advanced neural networks and deep learning",
                "duration": "20-24 weeks",
                "focus": ["deep_learning", "machine_learning", "programming"]
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run("learning_path:app", host="0.0.0.0", port=8003, reload=True)