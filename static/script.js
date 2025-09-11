// Global variables
let currentFile = null;
let currentOutputFile = null;

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const processBtn = document.getElementById('processBtn');
const processingSection = document.getElementById('processingSection');
const resultsSection = document.getElementById('resultsSection');
const resultMessage = document.getElementById('resultMessage');
const previewContainer = document.getElementById('previewContainer');
const downloadBtn = document.getElementById('downloadBtn');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const modelDetails = document.getElementById('modelDetails');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeDragAndDrop();
    loadModelInfo();
});

// Initialize drag and drop functionality
function initializeDragAndDrop() {
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', handleFileSelect);
    processBtn.addEventListener('click', processFile);
    downloadBtn.addEventListener('click', downloadFile);
}

// Drag and drop event handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File selection handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Handle file selection
function handleFile(file) {
    // Validate file type
    const allowedTypes = ['image/', 'video/'];
    const isValidType = allowedTypes.some(type => file.type.startsWith(type));
    
    if (!isValidType) {
        showError('Please select a valid image or video file.');
        return;
    }
    
    // Validate file size (100MB limit)
    if (file.size > 100 * 1024 * 1024) {
        showError('File size must be less than 100MB.');
        return;
    }
    
    currentFile = file;
    
    // Display file information
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    
    // Hide other sections
    hideAllSections();
    uploadArea.style.display = 'none';
}

// Process the selected file
async function processFile() {
    if (!currentFile) {
        showError('No file selected.');
        return;
    }
    
    // Show processing section
    hideAllSections();
    processingSection.style.display = 'block';
    
    try {
        const formData = new FormData();
        formData.append('file', currentFile);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentOutputFile = result.output_file;
            showResults(result.message, result.file_type);
        } else {
            showError(result.error || 'Processing failed.');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred while processing the file.');
    }
}

// Show results section
function showResults(message, fileType) {
    hideAllSections();
    resultsSection.style.display = 'block';
    
    resultMessage.textContent = message;
    
    // Create preview based on file type
    if (fileType === 'video') {
        const video = document.createElement('video');
        video.controls = true;
        video.src = `/download/${currentOutputFile}`;
        video.style.maxWidth = '100%';
        video.style.maxHeight = '400px';
        
        previewContainer.innerHTML = '';
        previewContainer.appendChild(video);
    } else {
        const img = document.createElement('img');
        img.src = `/download/${currentOutputFile}`;
        img.style.maxWidth = '100%';
        img.style.maxHeight = '400px';
        
        previewContainer.innerHTML = '';
        previewContainer.appendChild(img);
    }
}

// Download processed file
function downloadFile() {
    if (currentOutputFile) {
        const link = document.createElement('a');
        link.href = `/download/${currentOutputFile}`;
        link.download = currentOutputFile;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Show error section
function showError(message) {
    hideAllSections();
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

// Hide all sections
function hideAllSections() {
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Reset the application
function resetApp() {
    currentFile = null;
    currentOutputFile = null;
    
    // Reset file input
    fileInput.value = '';
    
    // Show upload section
    hideAllSections();
    uploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
    
    // Clear preview
    previewContainer.innerHTML = '';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Load model information
async function loadModelInfo() {
    try {
        const response = await fetch('/model-info');
        const modelInfo = await response.json();
        
        modelDetails.innerHTML = `
            <p><strong>Model:</strong> ${modelInfo.model_name}</p>
            <p><strong>Type:</strong> ${modelInfo.model_type}</p>
            <p><strong>Classes:</strong> ${Object.values(modelInfo.class_names).join(', ')}</p>
            <p><strong>Path:</strong> ${modelInfo.model_path}</p>
        `;
        
    } catch (error) {
        console.error('Error loading model info:', error);
        modelDetails.innerHTML = '<p>Error loading model information</p>';
    }
}

// Add some visual feedback for file processing
function updateProgress(progress) {
    const progressFill = document.getElementById('progressFill');
    if (progressFill) {
        progressFill.style.width = progress + '%';
    }
}

// Simulate progress for better UX
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }
        updateProgress(progress);
    }, 200);
}

// Enhanced error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showError('An unexpected error occurred. Please try again.');
});

// Add loading states
function setLoadingState(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.getAttribute('data-original-text') || element.innerHTML;
    }
}

// Store original button text
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.setAttribute('data-original-text', button.innerHTML);
    });
});
