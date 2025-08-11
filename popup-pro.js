// SummaBrowse Pro Extension - Professional JavaScript

class SummaBrowsePro {
    constructor() {
        this.apiUrl = 'https://summabrowser-api.onrender.com';
        this.currentTab = 'quick';
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkApiStatus();
        this.loadCurrentPageInfo();
        this.loadSettings();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.closest('.tab-btn').dataset.tab);
            });
        });

        // Quick Summary Actions
        document.getElementById('summarizeSelection')?.addEventListener('click', () => {
            this.summarizeSelection();
        });

        document.getElementById('summarizePage')?.addEventListener('click', () => {
            this.summarizePage();
        });

        // Page Analysis Actions
        document.getElementById('analyzeContent')?.addEventListener('click', () => {
            this.analyzePageContent();
        });

        document.getElementById('extractKeywords')?.addEventListener('click', () => {
            this.extractKeywords();
        });

        // Upload Actions
        document.getElementById('openWebApp')?.addEventListener('click', () => {
            this.openWebApp();
        });

        // Settings Actions
        document.getElementById('themeSelector')?.addEventListener('change', (e) => {
            this.changeTheme(e.target.value);
        });

        document.getElementById('notificationsToggle')?.addEventListener('change', (e) => {
            this.toggleNotifications(e.target.checked);
        });

        document.getElementById('resetSettings')?.addEventListener('click', () => {
            this.resetSettings();
        });

        // Modal Actions
        document.getElementById('closeModal')?.addEventListener('click', () => {
            this.hideModal();
        });

        document.getElementById('copyResult')?.addEventListener('click', () => {
            this.copyResult();
        });

        document.getElementById('openFullResult')?.addEventListener('click', () => {
            this.openFullResult();
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}Tab`).classList.add('active');

        this.currentTab = tabName;

        // Load tab-specific data
        if (tabName === 'page') {
            this.loadCurrentPageInfo();
        }
    }

    async checkApiStatus() {
        const statusElement = document.getElementById('apiStatus');
        const statusIndicator = document.getElementById('statusIndicator');

        try {
            const response = await fetch(`${this.apiUrl}/health`, { 
                method: 'GET',
                timeout: 5000 
            });
            
            if (response.ok) {
                statusElement.textContent = 'Online';
                statusElement.className = 'api-status';
                statusIndicator.innerHTML = '<i class="fas fa-circle" style="color: #10b981;"></i>';
                this.updateGlobalStatus('online');
            } else {
                throw new Error('Service unavailable');
            }
        } catch (error) {
            statusElement.textContent = 'Offline';
            statusElement.className = 'api-status offline';
            statusElement.style.background = '#fee2e2';
            statusElement.style.color = '#dc2626';
            statusIndicator.innerHTML = '<i class="fas fa-circle" style="color: #ef4444;"></i>';
            this.updateGlobalStatus('offline');
        }
    }

    async loadCurrentPageInfo() {
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const tab = tabs[0];

            if (tab) {
                const urlElement = document.getElementById('currentUrl');
                if (urlElement) {
                    const url = new URL(tab.url);
                    urlElement.textContent = url.hostname;
                }

                // Get page content for analysis
                chrome.tabs.sendMessage(tab.id, { action: 'getPageStats' }, (response) => {
                    if (response && !chrome.runtime.lastError) {
                        const wordCountElement = document.getElementById('wordCount');
                        const readTimeElement = document.getElementById('readTime');

                        if (wordCountElement && response.wordCount) {
                            wordCountElement.textContent = response.wordCount.toLocaleString();
                        }

                        if (readTimeElement && response.wordCount) {
                            const readTime = Math.ceil(response.wordCount / 200); // 200 WPM average
                            readTimeElement.textContent = `${readTime} min`;
                        }
                    }
                });
            }
        } catch (error) {
            console.error('Error loading page info:', error);
        }
    }

    async summarizeSelection() {
        this.showProcessing('Analyzing Selection', 'Processing selected text with AI');
        
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const tab = tabs[0];

            chrome.tabs.sendMessage(tab.id, { action: 'getSelection' }, async (response) => {
                if (response && response.text && response.text.trim()) {
                    const summary = await this.processSummary(response.text, 'selection');
                    this.hideProcessing();
                    this.showResult('Selection Summary', summary);
                } else {
                    this.hideProcessing();
                    this.showNotification('Please select some text first', 'error');
                }
            });
        } catch (error) {
            this.hideProcessing();
            this.showNotification('Error analyzing selection', 'error');
        }
    }

    async summarizePage() {
        this.showProcessing('Analyzing Page', 'Processing entire page content with AI');
        
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const tab = tabs[0];

            chrome.tabs.sendMessage(tab.id, { action: 'getPageContent' }, async (response) => {
                if (response && response.text) {
                    const summary = await this.processSummary(response.text, 'page');
                    this.hideProcessing();
                    this.showResult('Page Summary', summary);
                } else {
                    this.hideProcessing();
                    this.showNotification('Unable to extract page content', 'error');
                }
            });
        } catch (error) {
            this.hideProcessing();
            this.showNotification('Error analyzing page', 'error');
        }
    }

    async analyzePageContent() {
        this.showProcessing('Deep Analysis', 'Performing comprehensive content analysis');
        
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const tab = tabs[0];

            chrome.tabs.sendMessage(tab.id, { action: 'getPageContent' }, async (response) => {
                if (response && response.text) {
                    const analysis = await this.processAnalysis(response.text);
                    this.hideProcessing();
                    this.showResult('Content Analysis', analysis);
                } else {
                    this.hideProcessing();
                    this.showNotification('Unable to analyze page content', 'error');
                }
            });
        } catch (error) {
            this.hideProcessing();
            this.showNotification('Error during analysis', 'error');
        }
    }

    async extractKeywords() {
        this.showProcessing('Extracting Keywords', 'Identifying key terms and concepts');
        
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const tab = tabs[0];

            chrome.tabs.sendMessage(tab.id, { action: 'getPageContent' }, async (response) => {
                if (response && response.text) {
                    const keywords = await this.processKeywords(response.text);
                    this.hideProcessing();
                    this.showResult('Keywords Extracted', keywords);
                } else {
                    this.hideProcessing();
                    this.showNotification('Unable to extract keywords', 'error');
                }
            });
        } catch (error) {
            this.hideProcessing();
            this.showNotification('Error extracting keywords', 'error');
        }
    }

    async processSummary(text, type) {
        try {
            const summaryLength = document.querySelector('input[name="summaryLength"]:checked')?.value || 'brief';
            
            const response = await fetch(`${this.apiUrl}/process-text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    type: type,
                    length: summaryLength,
                    action: 'summarize'
                })
            });

            if (!response.ok) {
                throw new Error('Summary generation failed');
            }

            const data = await response.json();
            return data.summary || 'Summary generation completed successfully.';
        } catch (error) {
            return `Error: ${error.message}. Please try again or check your connection.`;
        }
    }

    async processAnalysis(text) {
        try {
            const response = await fetch(`${this.apiUrl}/process-text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    action: 'analyze'
                })
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const data = await response.json();
            return data.analysis || 'Content analysis completed successfully.';
        } catch (error) {
            return `Analysis Error: ${error.message}`;
        }
    }

    async processKeywords(text) {
        try {
            // Simple keyword extraction fallback
            const words = text.toLowerCase()
                .replace(/[^\w\s]/g, ' ')
                .split(/\s+/)
                .filter(word => word.length > 3);
            
            const wordCount = {};
            words.forEach(word => {
                wordCount[word] = (wordCount[word] || 0) + 1;
            });

            const keywords = Object.entries(wordCount)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 20)
                .map(([word, count]) => `${word} (${count})`)
                .join(', ');

            return `Key terms found: ${keywords}`;
        } catch (error) {
            return `Keyword extraction error: ${error.message}`;
        }
    }

    openWebApp() {
        chrome.tabs.create({ url: this.apiUrl });
        window.close();
    }

    showProcessing(title, description) {
        const overlay = document.getElementById('processingOverlay');
        const titleElement = document.getElementById('processingTitle');
        const descElement = document.getElementById('processingDescription');
        const progressFill = document.getElementById('progressFill');

        if (overlay && titleElement && descElement) {
            titleElement.textContent = title;
            descElement.textContent = description;
            overlay.classList.add('active');
            
            // Animate progress bar
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 10;
                if (progress > 90) progress = 90;
                progressFill.style.width = `${progress}%`;
            }, 200);

            this.progressInterval = interval;
            this.isProcessing = true;
        }
    }

    hideProcessing() {
        const overlay = document.getElementById('processingOverlay');
        const progressFill = document.getElementById('progressFill');

        if (overlay) {
            overlay.classList.remove('active');
            progressFill.style.width = '100%';
            
            setTimeout(() => {
                progressFill.style.width = '0%';
            }, 300);
        }

        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        this.isProcessing = false;
    }

    showResult(title, content) {
        const modal = document.getElementById('resultModal');
        const titleElement = document.getElementById('resultTitle');
        const contentElement = document.getElementById('resultContent');

        if (modal && titleElement && contentElement) {
            titleElement.textContent = title;
            contentElement.textContent = content;
            modal.classList.add('active');
            
            // Store result for copying
            this.lastResult = content;
        }
    }

    hideModal() {
        const modal = document.getElementById('resultModal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    async copyResult() {
        if (this.lastResult) {
            try {
                await navigator.clipboard.writeText(this.lastResult);
                this.showNotification('Result copied to clipboard!', 'success');
            } catch (error) {
                this.showNotification('Failed to copy result', 'error');
            }
        }
    }

    openFullResult() {
        this.openWebApp();
    }

    changeTheme(theme) {
        document.body.className = theme;
        this.saveSetting('theme', theme);
    }

    toggleNotifications(enabled) {
        this.saveSetting('notifications', enabled);
    }

    resetSettings() {
        if (confirm('Reset all settings to defaults?')) {
            chrome.storage.local.clear(() => {
                this.loadSettings();
                this.showNotification('Settings reset successfully', 'success');
            });
        }
    }

    loadSettings() {
        chrome.storage.local.get(['theme', 'notifications'], (result) => {
            const theme = result.theme || 'default';
            const notifications = result.notifications !== false;

            const themeSelector = document.getElementById('themeSelector');
            const notificationsToggle = document.getElementById('notificationsToggle');

            if (themeSelector) themeSelector.value = theme;
            if (notificationsToggle) notificationsToggle.checked = notifications;

            document.body.className = theme;
        });
    }

    saveSetting(key, value) {
        chrome.storage.local.set({ [key]: value });
    }

    updateGlobalStatus(status) {
        document.body.setAttribute('data-status', status);
    }

    showNotification(message, type = 'info') {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation' : 'info'}-circle"></i>
            <span>${message}</span>
        `;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 12px;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-in forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Content Script Communication Handler
if (typeof chrome !== 'undefined' && chrome.tabs) {
    // Inject content script if needed
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'ping' }, (response) => {
                if (chrome.runtime.lastError) {
                    // Content script not injected, inject it
                    chrome.scripting.executeScript({
                        target: { tabId: tabs[0].id },
                        function: injectContentScript
                    });
                }
            });
        }
    });
}

// Content Script Injection Function
function injectContentScript() {
    if (window.summaBrowseContentScript) return;
    
    window.summaBrowseContentScript = true;
    
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        try {
            switch (request.action) {
                case 'ping':
                    sendResponse({ status: 'ok' });
                    break;
                    
                case 'getSelection':
                    const selection = window.getSelection().toString();
                    sendResponse({ text: selection });
                    break;
                    
                case 'getPageContent':
                    // Get main content, avoiding nav, ads, etc.
                    const content = getMainContent();
                    const wordCount = content.split(/\s+/).filter(word => word.length > 0).length;
                    sendResponse({ text: content, wordCount });
                    break;
                    
                case 'getPageStats':
                    const pageContent = getMainContent();
                    const words = pageContent.split(/\s+/).filter(word => word.length > 0).length;
                    sendResponse({ wordCount: words });
                    break;
            }
        } catch (error) {
            sendResponse({ error: error.message });
        }
        
        return true; // Keep message channel open
    });
    
    function getMainContent() {
        // Try to get main content area
        const selectors = [
            'main article',
            'article',
            'main',
            '.content',
            '.post-content',
            '.entry-content',
            '#content',
            '.main-content'
        ];
        
        let content = '';
        
        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element) {
                content = element.innerText;
                break;
            }
        }
        
        // Fallback to body content
        if (!content) {
            content = document.body.innerText;
        }
        
        // Clean up the content
        return content
            .replace(/\s+/g, ' ')
            .replace(/\n\s*\n/g, '\n\n')
            .trim();
    }
}

// Initialize the extension
document.addEventListener('DOMContentLoaded', () => {
    window.summaBrowsePro = new SummaBrowsePro();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
