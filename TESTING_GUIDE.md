🔬 SummaBrowser Extension Testing Guide
==========================================

## Quick Setup (Do this first!)
1. **Load Extension in Chrome:**
   - Open Chrome and go to: `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right)
   - Click "Load unpacked"
   - Select the folder: `c:\Users\deepanshu.b\Downloads\Summa_Browser-main\Summa_Browser-main\SummaBrowse`
   - You should see "SummaBrowser - AI Document Summarizer" appear

2. **Pin the Extension:**
   - Click the puzzle piece icon (🧩) in Chrome toolbar
   - Find "SummaBrowser" and click the pin icon

## 🧪 Testing Scenarios

### Test 1: Connection Status Check
**What to test:** API connectivity
**Steps:**
1. Click the SummaBrowser extension icon
2. Look for status message at bottom
3. **Expected result:** "✅ Connected to SummaBrowser API"

### Test 2: Text Document Upload (Easy Test)
**What to test:** Basic file processing
**Steps:**
1. Click "Choose File" or drag the test document I created: `test-document.txt`
2. Click "📤 Process Document"
3. Wait for processing (should take 10-30 seconds)
4. **Expected results:**
   - Progress bar appears
   - Status shows "Uploading and processing file..."
   - Success message appears
   - Summary preview shows
   - Download link becomes available
   - Copy button works

### Test 3: Image with Text (OCR Test)
**Create a test image:**
1. Open any word processor (Word, Google Docs, etc.)
2. Type some text like:
   ```
   Welcome to AI Technology
   
   Machine learning is transforming industries.
   Natural language processing helps computers understand human text.
   Computer vision enables image recognition and analysis.
   ```
3. Take a screenshot or save as image (PNG/JPG)
4. **Test the image:**
   - Upload to SummaBrowser
   - Should extract text via OCR
   - Generate summary of extracted text

### Test 4: PDF Document Test
**Options for PDF testing:**
- Create a simple PDF with some text content
- Or use any existing PDF document
- Upload through the extension
- Verify text extraction and summarization

### Test 5: UI Features Testing
**Theme Toggle:**
- Click the 🌙/☀️ toggle
- Verify dark/light mode switching
- Refresh extension - theme should persist

**Drag & Drop:**
- Drag a file directly onto the drop zone
- Should highlight the area and accept the file

**File Validation:**
- Try uploading an unsupported file (e.g., .docx)
- Should show error toast message

## 🎯 What Success Looks Like

✅ **Green status:** "✅ Connected to SummaBrowser API"
✅ **File uploads:** No errors during upload
✅ **Processing works:** Shows progress and completes
✅ **Summary generated:** Text appears in preview area
✅ **Download works:** Can download the summary file
✅ **Copy function:** Can copy summary to clipboard
✅ **Themes work:** Dark/light mode toggle functions
✅ **Error handling:** Shows appropriate error messages for invalid files

## 🔍 Quick Test Commands

**Test the live API directly:**
```powershell
# Check API health
Invoke-WebRequest -Uri "https://summabrowser-api.onrender.com/health" -Method GET

# The response should be: {"status":"healthy","uptime":"online"}
```

## 🚨 Troubleshooting

**If extension doesn't load:**
- Check Developer Console (F12) for errors
- Ensure all files are in the correct folder
- Try removing and re-adding the extension

**If API connection fails:**
- Wait 30 seconds (Render free tier may sleep)
- Refresh the extension popup
- Check if status changes to "✅ Connected"

**If processing fails:**
- Check file size (must be < 16MB)
- Verify file type (PDF, JPG, PNG, etc.)
- Try a simpler document first

## 📁 Test Files Available
- `test-document.txt` - Ready-to-use text content
- Create your own images/PDFs for comprehensive testing

**Ready to test! Start with Test 1 and work through each scenario.**
