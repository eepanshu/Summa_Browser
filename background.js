// Background script for SummaBrowser
chrome.runtime.onInstalled.addListener(() => {
  console.log('SummaBrowser extension installed');
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.action.openPopup();
});

// Handle messages from content scripts or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getStorageData') {
    chrome.storage.local.get([request.key], (result) => {
      sendResponse(result);
    });
    return true; // Will respond asynchronously
  }
  
  if (request.action === 'setStorageData') {
    chrome.storage.local.set({[request.key]: request.value}, () => {
      sendResponse({success: true});
    });
    return true;
  }
});

// Set up context menu for right-click functionality (future enhancement)
chrome.contextMenus.create({
  id: "summarize-selection",
  title: "Summarize with SummaBrowser",
  contexts: ["selection"]
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "summarize-selection") {
    // Future: Handle text summarization from page selection
    chrome.action.openPopup();
  }
});
