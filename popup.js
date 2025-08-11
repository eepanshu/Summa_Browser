// SummaBrowser Enhanced Popup Script
class SummaBrowser {
  constructor() {
    this.init();
    this.selectedFile = null;
    this.isProcessing = false;
  }

  init() {
    this.bindEvents();
    this.loadTheme();
    this.checkBackendStatus();
  }

  bindEvents() {
    // File input events
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const fileDropArea = document.getElementById('fileDropArea');
    const removeFileBtn = document.getElementById('removeFile');
    const uploadButton = document.getElementById('uploadButton');
    
    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    
    // Copy button
    const copyBtn = document.getElementById('copyBtn');

    // Browse button click
    browseBtn.addEventListener('click', (e) => {
      e.preventDefault();
      fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
      this.handleFileSelect(e.target.files[0]);
    });

    // Drag and drop events
    fileDropArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      fileDropArea.classList.add('dragover');
    });

    fileDropArea.addEventListener('dragleave', () => {
      fileDropArea.classList.remove('dragover');
    });

    fileDropArea.addEventListener('drop', (e) => {
      e.preventDefault();
      fileDropArea.classList.remove('dragover');
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.handleFileSelect(files[0]);
      }
    });

    // Remove file button
    removeFileBtn.addEventListener('click', () => {
      this.clearFileSelection();
    });

    // Upload button
    uploadButton.addEventListener('click', () => {
      this.processFile();
    });

    // Theme toggle
    themeToggle.addEventListener('change', () => {
      this.toggleTheme();
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
      this.copyToClipboard();
    });
  }

  handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    const validTypes = [
      'application/pdf',
      'image/jpeg',
      'image/jpg', 
      'image/png',
      'image/gif',
      'image/bmp',
      'image/webp'
    ];

    if (!validTypes.includes(file.type)) {
      this.showToast('Please select a PDF or image file', 'error');
      return;
    }

    // Check file size (max 16MB)
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
      this.showToast('File size must be less than 16MB', 'error');
      return;
    }

    this.selectedFile = file;
    this.updateFileInfo(file);
    document.getElementById('uploadButton').disabled = false;
    this.clearStatus();
  }

  updateFileInfo(file) {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');

    fileName.textContent = file.name;
    fileSize.textContent = this.formatFileSize(file.size);
    fileInfo.style.display = 'block';
  }

  clearFileSelection() {
    this.selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('uploadButton').disabled = true;
    document.getElementById('resultSection').style.display = 'none';
    this.clearStatus();
  }

  async processFile() {
    if (!this.selectedFile || this.isProcessing) return;

    this.isProcessing = true;
    this.updateProcessButton(true);
    this.showProgress();
    this.updateStatus('Uploading and processing file...', 'info');

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }

      this.handleProcessSuccess(data);
    } catch (error) {
      this.handleProcessError(error.message);
    } finally {
      this.isProcessing = false;
      this.updateProcessButton(false);
      this.hideProgress();
    }
  }

  handleProcessSuccess(data) {
    this.updateStatus('File processed successfully!', 'success');
    this.showToast('Summary generated successfully!', 'success');
    
    // Update download link
    const downloadLink = document.getElementById('downloadLink');
    downloadLink.href = `http://127.0.0.1:5000${data.download_url}`;
    downloadLink.style.display = 'block';
    
    // Show summary preview
    const summaryPreview = document.getElementById('summaryPreview');
    const truncatedSummary = data.summary.length > 300 
      ? data.summary.substring(0, 300) + '...'
      : data.summary;
    summaryPreview.textContent = truncatedSummary;
    
    // Store full summary for copying
    this.fullSummary = data.summary;
    
    // Show result section
    document.getElementById('resultSection').style.display = 'block';
    document.getElementById('copyBtn').style.display = 'block';
  }

  handleProcessError(errorMessage) {
    this.updateStatus(`Error: ${errorMessage}`, 'error');
    this.showToast('Processing failed. Please try again.', 'error');
    document.getElementById('resultSection').style.display = 'none';
  }

  updateProcessButton(processing) {
    const uploadButton = document.getElementById('uploadButton');
    const btnText = uploadButton.querySelector('.btn-text');
    const btnLoader = uploadButton.querySelector('.btn-loader');

    if (processing) {
      btnText.style.display = 'none';
      btnLoader.style.display = 'block';
      uploadButton.disabled = true;
      uploadButton.classList.add('loading');
    } else {
      btnText.style.display = 'block';
      btnLoader.style.display = 'none';
      uploadButton.disabled = !this.selectedFile;
      uploadButton.classList.remove('loading');
    }
  }

  showProgress() {
    document.getElementById('progressBar').style.display = 'block';
  }

  hideProgress() {
    document.getElementById('progressBar').style.display = 'none';
  }

  updateStatus(message, type = '') {
    const statusElement = document.getElementById('status');
    statusElement.textContent = message;
    statusElement.className = `status-message ${type}`;
  }

  clearStatus() {
    const statusElement = document.getElementById('status');
    statusElement.textContent = '';
    statusElement.className = 'status-message';
  }

  toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-mode');
    
    // Save theme preference
    chrome.storage.local.set({ darkMode: isDark });
    
    // Update theme toggle icons
    this.updateThemeIcons(isDark);
  }

  loadTheme() {
    chrome.storage.local.get(['darkMode'], (result) => {
      const isDark = result.darkMode || false;
      if (isDark) {
        document.body.classList.add('dark-mode');
        document.getElementById('themeToggle').checked = true;
      }
      this.updateThemeIcons(isDark);
    });
  }

  updateThemeIcons(isDark) {
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');
    
    if (isDark) {
      sunIcon.style.opacity = '0.3';
      moonIcon.style.opacity = '1';
    } else {
      sunIcon.style.opacity = '1';
      moonIcon.style.opacity = '0.3';
    }
  }

  async copyToClipboard() {
    if (!this.fullSummary) return;

    try {
      await navigator.clipboard.writeText(this.fullSummary);
      this.showToast('Summary copied to clipboard!', 'success');
      
      // Visual feedback
      const copyBtn = document.getElementById('copyBtn');
      const originalText = copyBtn.innerHTML;
      copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
      
      setTimeout(() => {
        copyBtn.innerHTML = originalText;
      }, 2000);
    } catch (error) {
      this.showToast('Failed to copy to clipboard', 'error');
    }
  }

  async checkBackendStatus() {
    try {
      const response = await fetch('http://127.0.0.1:5000/', { method: 'GET' });
      if (!response.ok) {
        throw new Error('Backend not running');
      }
    } catch (error) {
      this.updateStatus('Backend server not running. Please start the Python server.', 'error');
      document.getElementById('uploadButton').disabled = true;
    }
  }

  showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastIcon = toast.querySelector('.toast-icon');
    const toastMessage = toast.querySelector('.toast-message');

    // Set icon based on type
    const icons = {
      success: 'fas fa-check-circle',
      error: 'fas fa-exclamation-circle',
      info: 'fas fa-info-circle'
    };

    toastIcon.className = `toast-icon ${icons[type]}`;
    toastMessage.textContent = message;
    toast.className = `toast ${type} show`;

    // Auto-hide after 4 seconds
    setTimeout(() => {
      toast.classList.remove('show');
    }, 4000);
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new SummaBrowser();
});