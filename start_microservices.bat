@echo off
echo Starting AI/ML Microservices Platform...
echo ====================================

echo.
echo Starting Text Summarization Service (Port 8001)...
start "Text Summarization" cmd /k "cd /d %~dp0 && python services/text_summarization.py"

timeout /t 2 > nul

echo Starting Q&A Documents Service (Port 8002)...
start "Q&A Documents" cmd /k "cd /d %~dp0 && python services/qa_documents.py"

timeout /t 2 > nul

echo Starting Learning Path Service (Port 8003)...
start "Learning Path" cmd /k "cd /d %~dp0 && python services/learning_path.py"

timeout /t 2 > nul

echo.
echo All microservices are starting...
echo.
echo Services will be available at:
echo - Text Summarization: http://localhost:8001
echo - Q&A Documents: http://localhost:8002  
echo - Learning Path: http://localhost:8003
echo - Main Website: http://localhost:8000
echo.
echo Press any key to continue...
pause > nul