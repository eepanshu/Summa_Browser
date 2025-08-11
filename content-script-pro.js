// SummaBrowse Pro Content Script
// This script runs on all web pages to enable content extraction and analysis

(function() {
    'use strict';
    
    // Avoid multiple injections
    if (window.summaBrowseProContentScript) {
        return;
    }
    window.summaBrowseProContentScript = true;
    
    class ContentExtractor {
        constructor() {
            this.setupMessageListener();
            this.addVisualIndicators();
        }
        
        setupMessageListener() {
            chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
                try {
                    switch (request.action) {
                        case 'ping':
                            sendResponse({ status: 'active', version: '3.0.0' });
                            break;
                            
                        case 'getSelection':
                            const selection = this.getSelectedText();
                            sendResponse({ 
                                text: selection.text,
                                html: selection.html,
                                length: selection.text.length
                            });
                            break;
                            
                        case 'getPageContent':
                            const content = this.extractPageContent();
                            sendResponse({
                                text: content.text,
                                html: content.html,
                                wordCount: content.wordCount,
                                title: document.title,
                                url: window.location.href
                            });
                            break;
                            
                        case 'getPageStats':
                            const stats = this.getPageStatistics();
                            sendResponse(stats);
                            break;
                            
                        case 'highlightText':
                            this.highlightText(request.text);
                            sendResponse({ success: true });
                            break;
                            
                        case 'clearHighlights':
                            this.clearHighlights();
                            sendResponse({ success: true });
                            break;
                    }
                } catch (error) {
                    console.error('SummaBrowse Pro Content Script Error:', error);
                    sendResponse({ error: error.message });
                }
                
                return true; // Keep message channel open for async responses
            });
        }
        
        getSelectedText() {
            const selection = window.getSelection();
            const selectedText = selection.toString().trim();
            
            let selectedHtml = '';
            if (selection.rangeCount > 0) {
                const container = document.createElement('div');
                container.appendChild(selection.getRangeAt(0).cloneContents());
                selectedHtml = container.innerHTML;
            }
            
            return {
                text: selectedText,
                html: selectedHtml,
                length: selectedText.length
            };
        }
        
        extractPageContent() {
            // Advanced content extraction with multiple fallback strategies
            const extractors = [
                () => this.extractFromJsonLd(),
                () => this.extractFromArticle(),
                () => this.extractFromMain(),
                () => this.extractFromContentSelectors(),
                () => this.extractFromBody()
            ];
            
            let bestContent = { text: '', html: '', score: 0 };
            
            for (const extractor of extractors) {
                try {
                    const content = extractor();
                    if (content && content.score > bestContent.score) {
                        bestContent = content;
                    }
                } catch (error) {
                    console.warn('Content extraction method failed:', error);
                }
            }
            
            const wordCount = this.countWords(bestContent.text);
            
            return {
                text: bestContent.text,
                html: bestContent.html,
                wordCount: wordCount,
                extractionMethod: bestContent.method || 'unknown'
            };
        }
        
        extractFromJsonLd() {
            const jsonLdScripts = document.querySelectorAll('script[type="application/ld+json"]');
            
            for (const script of jsonLdScripts) {
                try {
                    const data = JSON.parse(script.textContent);
                    if (data.articleBody || data.text) {
                        const text = data.articleBody || data.text;
                        return {
                            text: text,
                            html: `<p>${text}</p>`,
                            score: 95,
                            method: 'json-ld'
                        };
                    }
                } catch (error) {
                    continue;
                }
            }
            return null;
        }
        
        extractFromArticle() {
            const articles = document.querySelectorAll('article');
            if (articles.length > 0) {
                const article = articles[0];
                const text = this.cleanText(article.innerText);
                return {
                    text: text,
                    html: article.innerHTML,
                    score: 90,
                    method: 'article-tag'
                };
            }
            return null;
        }
        
        extractFromMain() {
            const main = document.querySelector('main');
            if (main) {
                const text = this.cleanText(main.innerText);
                if (text.length > 200) {
                    return {
                        text: text,
                        html: main.innerHTML,
                        score: 85,
                        method: 'main-tag'
                    };
                }
            }
            return null;
        }
        
        extractFromContentSelectors() {
            const selectors = [
                '.post-content',
                '.entry-content',
                '.article-content',
                '.content-body',
                '.post-body',
                '.article-body',
                '#content',
                '.content',
                '.main-content',
                '[role="main"]'
            ];
            
            for (const selector of selectors) {
                const element = document.querySelector(selector);
                if (element) {
                    const text = this.cleanText(element.innerText);
                    if (text.length > 100) {
                        return {
                            text: text,
                            html: element.innerHTML,
                            score: 80,
                            method: `selector-${selector}`
                        };
                    }
                }
            }
            return null;
        }
        
        extractFromBody() {
            // Last resort - extract from body but filter out navigation, ads, etc.
            const body = document.body.cloneNode(true);
            
            // Remove unwanted elements
            const unwantedSelectors = [
                'nav', 'header', 'footer', 'aside',
                '.navigation', '.nav', '.menu',
                '.sidebar', '.widget', '.ad', '.advertisement',
                '.social', '.share', '.comments',
                'script', 'style', 'noscript'
            ];
            
            unwantedSelectors.forEach(selector => {
                const elements = body.querySelectorAll(selector);
                elements.forEach(el => el.remove());
            });
            
            const text = this.cleanText(body.innerText);
            return {
                text: text,
                html: body.innerHTML,
                score: 50,
                method: 'body-filtered'
            };
        }
        
        getPageStatistics() {
            const content = this.extractPageContent();
            const readingTime = Math.ceil(content.wordCount / 200); // 200 WPM average
            
            return {
                title: document.title,
                url: window.location.href,
                domain: window.location.hostname,
                wordCount: content.wordCount,
                readingTime: readingTime,
                characterCount: content.text.length,
                extractionMethod: content.extractionMethod,
                language: document.documentElement.lang || 'unknown'
            };
        }
        
        cleanText(text) {
            return text
                .replace(/\s+/g, ' ')                    // Multiple spaces to single
                .replace(/\n\s*\n\s*\n/g, '\n\n')       // Multiple newlines to double
                .replace(/^\s+|\s+$/g, '')               // Trim
                .replace(/[\u200B-\u200D\uFEFF]/g, '');  // Remove zero-width characters
        }
        
        countWords(text) {
            if (!text) return 0;
            return text.trim().split(/\s+/).filter(word => word.length > 0).length;
        }
        
        highlightText(searchText) {
            this.clearHighlights();
            
            if (!searchText || searchText.length < 2) return;
            
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );
            
            const textNodes = [];
            let node;
            while (node = walker.nextNode()) {
                if (node.textContent.toLowerCase().includes(searchText.toLowerCase())) {
                    textNodes.push(node);
                }
            }
            
            textNodes.forEach(textNode => {
                const parent = textNode.parentNode;
                const text = textNode.textContent;
                const regex = new RegExp(`(${this.escapeRegex(searchText)})`, 'gi');
                
                if (regex.test(text)) {
                    const highlightedHTML = text.replace(regex, 
                        '<mark class="summabrowse-highlight" style="background-color: #fef08a; padding: 2px 4px; border-radius: 3px;">$1</mark>'
                    );
                    
                    const wrapper = document.createElement('span');
                    wrapper.innerHTML = highlightedHTML;
                    parent.replaceChild(wrapper, textNode);
                }
            });
        }
        
        clearHighlights() {
            const highlights = document.querySelectorAll('.summabrowse-highlight');
            highlights.forEach(highlight => {
                const parent = highlight.parentNode;
                parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
                parent.normalize();
            });
        }
        
        escapeRegex(string) {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }
        
        addVisualIndicators() {
            // Add subtle visual indicator when SummaBrowse is active
            if (document.querySelector('.summabrowse-indicator')) return;
            
            const indicator = document.createElement('div');
            indicator.className = 'summabrowse-indicator';
            indicator.innerHTML = '🤖';
            indicator.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                width: 24px;
                height: 24px;
                background: rgba(102, 126, 234, 0.9);
                color: white;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                z-index: 10000;
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            `;
            
            document.body.appendChild(indicator);
            
            // Show indicator briefly when extension is used
            this.showIndicator = () => {
                indicator.style.opacity = '1';
                setTimeout(() => {
                    indicator.style.opacity = '0';
                }, 2000);
            };
        }
    }
    
    // Initialize content extractor
    const extractor = new ContentExtractor();
    
    // Global reference for debugging
    window.summaBrowseExtractor = extractor;
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl+Shift+S - Summarize selection
        if (e.ctrlKey && e.shiftKey && e.code === 'KeyS') {
            e.preventDefault();
            const selection = extractor.getSelectedText();
            if (selection.text.length > 0) {
                chrome.runtime.sendMessage({
                    action: 'summarizeSelection',
                    text: selection.text
                });
                extractor.showIndicator?.();
            }
        }
        
        // Ctrl+Shift+P - Summarize page
        if (e.ctrlKey && e.shiftKey && e.code === 'KeyP') {
            e.preventDefault();
            chrome.runtime.sendMessage({
                action: 'summarizePage'
            });
            extractor.showIndicator?.();
        }
    });
    
    // Handle selection changes for potential analysis
    document.addEventListener('selectionchange', () => {
        const selection = window.getSelection();
        if (selection.toString().length > 50) {
            // Could trigger analysis preview here
        }
    });
    
    console.log('SummaBrowse Pro Content Script v3.0.0 loaded');
    
})();
