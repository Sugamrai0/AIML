// Global variables and configuration
const API_BASE_URL = 'http://localhost:8000';
const SERVICES = {
    textSummary: 'http://localhost:8001',
    qaDocuments: 'http://localhost:8002',
    learningPath: 'http://localhost:8003',
    flowise: 'http://localhost:3000'
};

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
    checkServiceStatus();
    setupEventListeners();
    setupNavigationScroll();
});

// Initialize website functionality
function initializeWebsite() {
    // Initialize demo tabs
    setupDemoTabs();
    
    // Setup file upload handlers
    setupFileUploads();
    
    // Initialize responsive navigation
    setupMobileNavigation();
    
    // Setup smooth scrolling
    setupSmoothScrolling();
    
    console.log('AI/ML Platform website initialized successfully');
}

// Setup demo tabs functionality
function setupDemoTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const demoContents = document.querySelectorAll('.demo-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            demoContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Setup file upload handlers
function setupFileUploads() {
    // Summary file upload
    const summaryFileInput = document.getElementById('summaryFile');
    if (summaryFileInput) {
        summaryFileInput.addEventListener('change', handleSummaryFileUpload);
    }
    
    // Q&A file upload
    const qaFileInput = document.getElementById('qaFile');
    if (qaFileInput) {
        qaFileInput.addEventListener('change', handleQAFileUpload);
    }
}

// Setup mobile navigation
function setupMobileNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
}

// Setup smooth scrolling
function setupSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                scrollToSection(targetId);
            }
        });
    });
}

// Setup navigation scroll effects
function setupNavigationScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(15, 15, 35, 0.98)';
        } else {
            navbar.style.background = 'rgba(15, 15, 35, 0.95)';
        }
    });
}

// Setup additional event listeners
function setupEventListeners() {
    // Neural network animation
    animateNeuralNetwork();
    
    // Service status check interval
    setInterval(checkServiceStatus, 30000); // Check every 30 seconds
}

// Scroll to section functionality
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        const offsetTop = element.offsetTop - 80; // Account for fixed navbar
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// Show loading overlay
function showLoading(message = 'Processing with AI...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = overlay.querySelector('p');
    loadingText.textContent = message;
    overlay.classList.add('active');
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('active');
}

// Check service status
async function checkServiceStatus() {
    const statusIndicators = document.querySelectorAll('.status-indicator');
    
    try {
        // Check main API
        const mainResponse = await fetch(`${API_BASE_URL}/health`);
        updateServiceStatus('main', mainResponse.ok);
        
        // Check individual services
        for (const [service, url] of Object.entries(SERVICES)) {
            try {
                const response = await fetch(`${url}/health`);
                updateServiceStatus(service, response.ok);
            } catch (error) {
                updateServiceStatus(service, false);
            }
        }
    } catch (error) {
        console.error('Error checking service status:', error);
        statusIndicators.forEach(indicator => {
            indicator.classList.remove('online');
            indicator.classList.add('offline');
        });
    }
}

// Update service status indicators
function updateServiceStatus(service, isOnline) {
    const indicators = document.querySelectorAll('.status-indicator');
    indicators.forEach(indicator => {
        if (isOnline) {
            indicator.classList.remove('offline');
            indicator.classList.add('online');
        } else {
            indicator.classList.remove('online');
            indicator.classList.add('offline');
        }
    });
}

// Text Summarization Functions
async function summarizeText() {
    const textInput = document.getElementById('summaryText');
    const resultContainer = document.getElementById('summaryResult');
    
    if (!textInput.value.trim()) {
        showError(resultContainer, 'Please enter text to summarize');
        return;
    }
    
    showLoading('Generating AI summary...');
    
    try {
        const response = await fetch(`${SERVICES.textSummary}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: textInput.value
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            displaySummaryResult(resultContainer, result.summary);
        } else {
            throw new Error(`Server error: ${response.status}`);
        }
    } catch (error) {
        console.error('Error summarizing text:', error);
        showError(resultContainer, 'Failed to generate summary. Please check if the text summarization service is running.');
    } finally {
        hideLoading();
    }
}

// Handle summary file upload
function handleSummaryFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        uploadDocumentForSummary(file);
    }
}

// Upload document for summarization
async function uploadDocumentForSummary(file) {
    const resultContainer = document.getElementById('summaryResult');
    
    showLoading('Processing document...');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${SERVICES.textSummary}/summarize-document`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            displaySummaryResult(resultContainer, result.summary);
        } else {
            throw new Error(`Server error: ${response.status}`);
        }
    } catch (error) {
        console.error('Error processing document:', error);
        showError(resultContainer, 'Failed to process document. Please check the file format and try again.');
    } finally {
        hideLoading();
    }
}

// Display summary result
function displaySummaryResult(container, summary) {
    container.innerHTML = `
        <div class="result-content">
            <div class="result-header">
                <i class="fas fa-check-circle" style="color: var(--success-color);"></i>
                <span>Summary Generated</span>
            </div>
            <div class="result-text">${summary}</div>
            <div class="result-actions">
                <button class="btn btn-secondary" onclick="copySummaryResult()">
                    <i class="fas fa-copy"></i>Copy Result
                </button>
            </div>
        </div>
    `;
}

// Q&A Document Functions
function uploadDocument(type) {
    const fileInput = document.getElementById(`${type}File`);
    fileInput.click();
}

// Handle Q&A file upload
function handleQAFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        uploadDocumentForQA(file);
    }
}

// Upload document for Q&A
async function uploadDocumentForQA(file) {
    const uploadArea = document.getElementById('qaUploadArea');
    const questionSection = document.getElementById('questionSection');
    
    showLoading('Uploading and processing document...');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${SERVICES.qaDocuments}/upload-document`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            uploadArea.innerHTML = `
                <div class="upload-success">
                    <i class="fas fa-check-circle" style="color: var(--success-color);"></i>
                    <p>Document uploaded: ${file.name}</p>
                    <button class="btn btn-secondary" onclick="uploadDocument('qa')">Upload Another</button>
                </div>
            `;
            questionSection.style.display = 'block';
        } else {
            throw new Error(`Server error: ${response.status}`);
        }
    } catch (error) {
        console.error('Error uploading document:', error);
        showError(uploadArea, 'Failed to upload document. Please check the file format and try again.');
    } finally {
        hideLoading();
    }
}

// Ask question about document
async function askQuestion() {
    const questionInput = document.getElementById('questionText');
    const resultContainer = document.getElementById('qaResult');
    
    if (!questionInput.value.trim()) {
        showError(resultContainer, 'Please enter a question');
        return;
    }
    
    showLoading('Finding answer in document...');
    
    try {
        const response = await fetch(`${SERVICES.qaDocuments}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: questionInput.value
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            displayQAResult(resultContainer, result);
        } else {
            throw new Error(`Server error: ${response.status}`);
        }
    } catch (error) {
        console.error('Error asking question:', error);
        showError(resultContainer, 'Failed to get answer. Please ensure a document is uploaded and the Q&A service is running.');
    } finally {
        hideLoading();
    }
}

// Display Q&A result
function displayQAResult(container, result) {
    container.innerHTML = `
        <div class="result-content">
            <div class="result-header">
                <i class="fas fa-question-circle" style="color: var(--accent-color);"></i>
                <span>Question Answered</span>
            </div>
            <div class="qa-question">
                <strong>Q:</strong> ${result.question}
            </div>
            <div class="qa-answer">
                <strong>A:</strong> ${result.answer}
            </div>
            ${result.sources ? `
                <div class="qa-sources">
                    <strong>Sources:</strong> ${result.sources.join(', ')}
                </div>
            ` : ''}
            <div class="result-actions">
                <button class="btn btn-secondary" onclick="copyQAResult()">
                    <i class="fas fa-copy"></i>Copy Answer
                </button>
            </div>
        </div>
    `;
}

// Learning Path Functions
async function generateLearningPath() {
    const goalInput = document.getElementById('learningGoal');
    const experienceLevel = document.getElementById('experienceLevel').value;
    const timeCommitment = document.getElementById('timeCommitment').value;
    const resultContainer = document.getElementById('learningResult');
    
    if (!goalInput.value.trim()) {
        showError(resultContainer, 'Please describe your learning goals');
        return;
    }
    
    showLoading('Generating personalized learning path...');
    
    try {
        const response = await fetch(`${SERVICES.learningPath}/suggest-path-json`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                goals: goalInput.value,
                experience_level: experienceLevel,
                time_commitment: timeCommitment
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            displayLearningPathResult(resultContainer, result);
        } else {
            throw new Error(`Server error: ${response.status}`);
        }
    } catch (error) {
        console.error('Error generating learning path:', error);
        showError(resultContainer, 'Failed to generate learning path. Please check if the learning path service is running.');
    } finally {
        hideLoading();
    }
}

// Display learning path result
function displayLearningPathResult(container, result) {
    const learningPath = result.learning_path || result.path || 'Generated learning path would appear here';
    
    container.innerHTML = `
        <div class="result-content">
            <div class="result-header">
                <i class="fas fa-graduation-cap" style="color: var(--success-color);"></i>
                <span>Learning Path Generated</span>
            </div>
            <div class="learning-path-content">
                ${formatLearningPath(learningPath)}
            </div>
            <div class="result-actions">
                <button class="btn btn-secondary" onclick="copyLearningPath()">
                    <i class="fas fa-copy"></i>Copy Learning Path
                </button>
                <button class="btn btn-primary" onclick="exportLearningPath()">
                    <i class="fas fa-download"></i>Export as PDF
                </button>
            </div>
        </div>
    `;
}

// Format learning path content
function formatLearningPath(content) {
    if (typeof content === 'string') {
        return `<div class="learning-path-text">${content}</div>`;
    }
    
    // If it's structured data, format accordingly
    if (content.phases || content.steps) {
        let formatted = '<div class="learning-phases">';
        const phases = content.phases || content.steps;
        
        phases.forEach((phase, index) => {
            formatted += `
                <div class="learning-phase">
                    <h5>Phase ${index + 1}: ${phase.title || phase.name}</h5>
                    <p>${phase.description}</p>
                    ${phase.duration ? `<span class="phase-duration">${phase.duration}</span>` : ''}
                </div>
            `;
        });
        
        formatted += '</div>';
        return formatted;
    }
    
    return `<div class="learning-path-text">${JSON.stringify(content, null, 2)}</div>`;
}

// Flowise Integration Functions
function openFlowise() {
    window.open(SERVICES.flowise, '_blank');
}

// SSO Demonstration Functions
function demonstrateSSO(provider) {
    const authStatus = document.getElementById('authStatus');
    
    showLoading(`Simulating ${provider} SSO authentication...`);
    
    // Simulate authentication process
    setTimeout(() => {
        hideLoading();
        
        authStatus.innerHTML = `
            <div class="auth-indicator">
                <span class="status-indicator online"></span>
                <span>Authenticated via ${provider.charAt(0).toUpperCase() + provider.slice(1)}</span>
            </div>
            <div class="auth-details">
                <div class="user-info">
                    <strong>User:</strong> demo.user@example.com<br>
                    <strong>Provider:</strong> ${provider}<br>
                    <strong>Session:</strong> Active<br>
                    <strong>Scope:</strong> read, write, ai-services
                </div>
                <div class="auth-actions">
                    <button class="btn btn-secondary" onclick="simulateLogout()">
                        <i class="fas fa-sign-out-alt"></i>Logout
                    </button>
                </div>
            </div>
        `;
    }, 2000);
}

// Simulate logout
function simulateLogout() {
    const authStatus = document.getElementById('authStatus');
    
    authStatus.innerHTML = `
        <div class="auth-indicator">
            <span class="status-indicator offline"></span>
            <span>Not Authenticated</span>
        </div>
        <div class="auth-details">
            <p>Click on any provider above to simulate SSO authentication flow</p>
        </div>
    `;
}

// Documentation Functions
function openSwaggerDocs() {
    window.open(`${API_BASE_URL}/docs`, '_blank');
}

function downloadPostmanCollection() {
    // Create a simple Postman collection
    const collection = {
        info: {
            name: "AI/ML Microservices API",
            description: "API collection for AI/ML microservices platform"
        },
        item: [
            {
                name: "Text Summarization",
                request: {
                    method: "POST",
                    header: [{"key": "Content-Type", "value": "application/json"}],
                    url: `${SERVICES.textSummary}/summarize`,
                    body: {
                        mode: "raw",
                        raw: JSON.stringify({text: "Your text here"})
                    }
                }
            }
        ]
    };
    
    const blob = new Blob([JSON.stringify(collection, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'AI-ML-Microservices.postman_collection.json';
    a.click();
    URL.revokeObjectURL(url);
}

// Utility Functions
function showError(container, message) {
    container.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-triangle" style="color: var(--error-color);"></i>
            <p>${message}</p>
        </div>
    `;
}

function copySummaryResult() {
    const resultText = document.querySelector('#summaryResult .result-text');
    if (resultText) {
        copyToClipboard(resultText.textContent);
        showToast('Summary copied to clipboard!');
    }
}

function copyQAResult() {
    const answer = document.querySelector('#qaResult .qa-answer');
    if (answer) {
        copyToClipboard(answer.textContent);
        showToast('Answer copied to clipboard!');
    }
}

function copyLearningPath() {
    const learningPath = document.querySelector('#learningResult .learning-path-content');
    if (learningPath) {
        copyToClipboard(learningPath.textContent);
        showToast('Learning path copied to clipboard!');
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Text copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--success-color);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        z-index: 10000;
        box-shadow: var(--shadow-lg);
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function exportLearningPath() {
    showToast('PDF export feature coming soon!');
}

// Animate neural network background
function animateNeuralNetwork() {
    const neuralNetwork = document.querySelector('.neural-network');
    if (neuralNetwork) {
        // Add dynamic nodes
        for (let i = 0; i < 20; i++) {
            const node = document.createElement('div');
            node.className = 'neural-node';
            node.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(99, 102, 241, 0.6);
                border-radius: 50%;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
            `;
            neuralNetwork.appendChild(node);
        }
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.6; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
    }
    
    .result-content {
        padding: 1rem;
    }
    
    .result-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .result-text, .qa-answer, .learning-path-text {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        line-height: 1.6;
    }
    
    .qa-question {
        background: var(--bg-primary);
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid var(--accent-color);
    }
    
    .qa-sources {
        margin-top: 1rem;
        padding: 0.5rem;
        background: var(--bg-secondary);
        border-radius: 0.5rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .result-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .error-message {
        text-align: center;
        color: var(--error-color);
        padding: 2rem;
    }
    
    .error-message i {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .upload-success {
        text-align: center;
        color: var(--success-color);
        padding: 2rem;
    }
    
    .learning-phases {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .learning-phase {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--secondary-color);
    }
    
    .learning-phase h5 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .phase-duration {
        background: var(--bg-tertiary);
        color: var(--accent-color);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .user-info {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.875rem;
    }
    
    .auth-actions {
        margin-top: 1rem;
    }
`;
document.head.appendChild(style);

console.log('AI/ML Platform JavaScript loaded successfully');