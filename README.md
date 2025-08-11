# SummaBrowser - AI Document Summarizer

<div align="center">
  <img src="icons/icon128.png" alt="SummaBrowser Logo" width="128" height="128">
  <h3>🧠 Intelligent document summarization powered by AI</h3>
  <p>A powerful browser extension that processes PDFs and images to generate concise, intelligent summaries.</p>
</div>

## ✨ Features

- **🔍 Multi-format Support**: Process PDFs and various image formats (PNG, JPG, JPEG, GIF, BMP, WebP)
- **🧠 AI-Powered Summarization**: Advanced text extraction and summarization using OCR and NLP
- **🎨 Modern UI/UX**: Beautiful, responsive interface with dark/light mode support
- **📱 Drag & Drop**: Intuitive file upload with drag-and-drop functionality
- **📋 Quick Actions**: Copy summaries to clipboard or download as text files
- **⚡ Real-time Processing**: Live progress indicators and status updates
- **🔒 Privacy First**: All processing happens locally on your machine
- **🚀 Fast & Efficient**: Optimized for quick document processing

## 🛠️ Technology Stack

### Frontend (Browser Extension)
- **Manifest V3**: Latest Chrome extension architecture
- **Modern CSS**: CSS Grid, Flexbox, CSS Variables, and animations
- **Vanilla JavaScript**: ES6+ with async/await and modern APIs
- **Font Awesome**: Beautiful icons and visual elements

### Backend (Python Server)
- **Flask**: Lightweight web framework
- **Tesseract OCR**: Text extraction from images
- **Pillow**: Image processing and manipulation
- **Custom NLP**: Text summarization algorithms

## 📦 Installation

### Prerequisites
- Google Chrome or Chromium-based browser
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/eepanshu/Summa_Browser.git
cd Summa_Browser
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
cd SummaBrowse/summary
pip install -r requirements.txt
```

### Step 3: Install Tesseract OCR
- **Windows**: Download from [GitHub releases](https://github.com/tesseract-ocr/tesseract/releases)
- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`

### Step 4: Load Extension in Browser
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked"
4. Select the `SummaBrowse` folder
5. The SummaBrowser extension should now appear in your browser

### Step 5: Start the Backend Server
```bash
cd SummaBrowse/summary
python app.py
```
The server will start on `http://127.0.0.1:5000`

## 🚀 Usage

1. **Start the Backend**: Ensure the Python server is running
2. **Open Extension**: Click the SummaBrowser icon in your browser toolbar
3. **Upload File**: 
   - Drag and drop a file onto the upload area, or
   - Click "Browse Files" to select a document
4. **Process**: Click "Process Document" to start summarization
5. **Get Results**: 
   - View the summary preview
   - Download the full summary as a text file
   - Copy the summary to your clipboard

## 🎯 Supported File Types

- **PDFs**: `.pdf`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`

## 📁 Project Structure

```
SummaBrowse/
├── manifest.json          # Extension configuration
├── popup.html            # Main UI interface
├── popup.js              # Frontend JavaScript logic
├── styles.css            # Modern CSS styling
├── background.js         # Service worker script
├── icons/                # Extension icons
│   ├── icon16.png
│   ├── icon32.png
│   ├── icon48.png
│   └── icon128.png
├── summary/              # Python backend
│   ├── app.py           # Flask application
│   ├── requirements.txt # Python dependencies
│   ├── text_extraction_and_summarization.py
│   ├── process_pdf.py
│   ├── templates/
│   ├── uploads/         # Uploaded files
│   └── output/          # Generated summaries
└── README.md            # This file
```

## ⚙️ Configuration

### Backend Server
The Flask server runs on `http://127.0.0.1:5000` by default. To change this:

1. Edit `app.py` to modify host and port
2. Update the `host_permissions` in `manifest.json`
3. Update the API endpoints in `popup.js`

### File Size Limits
- Default: 16MB maximum file size
- Modify `MAX_CONTENT_LENGTH` in `app.py` to change this limit

### Supported Languages (OCR)
Tesseract supports 100+ languages. To add language support:

```bash
# Install additional language packs
# Example for Spanish:
sudo apt-get install tesseract-ocr-spa
```

## 🔧 Development

### Adding New Features
1. **Frontend**: Modify `popup.html`, `popup.js`, and `styles.css`
2. **Backend**: Add new routes in `app.py`
3. **Processing**: Extend functionality in the processing modules

### Testing
```bash
# Test the Flask backend
cd SummaBrowse/summary
python -m pytest tests/

# Load extension in development mode
# Use Chrome Developer Tools for frontend debugging
```

### Building for Production
1. Optimize images and assets
2. Minify CSS and JavaScript
3. Update version in `manifest.json`
4. Package the extension for Chrome Web Store

## 🐛 Troubleshooting

### Common Issues

**Extension not loading:**
- Ensure manifest.json is valid JSON
- Check that all required files exist
- Verify Chrome Developer Mode is enabled

**Backend connection failed:**
- Verify Python server is running on port 5000
- Check firewall settings
- Ensure all dependencies are installed

**OCR not working:**
- Verify Tesseract is properly installed
- Check image quality and resolution
- Ensure supported file format

**Processing errors:**
- Check file size (must be < 16MB)
- Verify file is not corrupted
- Check server logs for detailed errors

### Debug Mode
Enable debug mode in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/eepanshu/Summa_Browser/issues) page
2. Create a new issue with detailed description
3. Include system information and error logs

## 🔮 Roadmap

- [ ] **Multi-language Support**: UI localization
- [ ] **Cloud Integration**: Google Drive, Dropbox support
- [ ] **Advanced Summarization**: Custom summary lengths
- [ ] **Batch Processing**: Multiple file processing
- [ ] **Export Options**: PDF, DOCX, HTML export
- [ ] **Search & History**: Search through processed documents
- [ ] **API Integration**: Support for external AI services
- [ ] **Mobile Support**: Progressive Web App version

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Font Awesome](https://fontawesome.com/) for beautiful icons
- [Google Fonts](https://fonts.google.com/) for typography

---

<div align="center">
  <p>Made with ❤️ by the SummaBrowser Team</p>
  <p>⭐ Star this repo if you find it helpful!</p>
</div>
