# SummaBrowser - AI Document Summarizer

<div align="center">
  <img src="icons/icon128.png" alt="SummaBrowser Logo" width="128" height="128">
  <h3>🧠 Intelligent document summarization powered by AI</h3>
  <p>A powerful browser extension and web application that processes PDFs, images, and documents to generate concise, intelligent summaries.</p>
  
  <h2>🚀 **LIVE DEMO** 🚀</h2>
  <p>
    <a href="https://summabrowser-api.onrender.com" target="_blank">
      <img src="https://img.shields.io/badge/Try%20Live%20Demo-🌐%20summabrowser--api.onrender.com-brightgreen?style=for-the-badge&logo=render" alt="Live Demo">
    </a>
  </p>
  <p><strong>✨ No installation required! Try the web version instantly.</strong></p>
</div>

## 🌟 **New! Web Interface Available**

**🌐 Live Web App:** https://summabrowser-api.onrender.com

Experience SummaBrowser directly in your browser with our beautiful web interface:
- 🎨 **Modern UI Design** with drag-and-drop functionality
- � **Fully Responsive** - works on desktop, tablet, and mobile
- ⚡ **Real-time Processing** with progress indicators
- 🤖 **AI-Powered Summarization** with OCR capabilities
- 📊 **Processing Stats** and performance metrics
- 📥 **Download & Copy** functionality

## ✨ Features

### 🔥 **Core Capabilities**
- **🔍 Multi-format Support**: Process PDFs, images (PNG, JPG, JPEG, GIF, BMP, WebP), and text files
- **🧠 Advanced AI Summarization**: Intelligent text extraction with sentence scoring and ranking
- **👁️ OCR Technology**: Extract text from images using online OCR APIs
- **📄 PDF Processing**: Multi-page PDF text extraction with advanced parsing

### 🎨 **User Experience**
- **🌐 Web Interface**: Beautiful standalone web application
- **🔌 Browser Extension**: Chrome/Edge extension for seamless integration
- **🎯 Drag & Drop**: Intuitive file upload with visual feedback
- **🌓 Theme Support**: Dark and light mode with smooth transitions
- **📋 Quick Actions**: Copy to clipboard, download summaries, real-time status

### ⚡ **Performance & Reliability**
- **🚀 Live Deployment**: Production-ready on Render.com
- **🔒 Secure Processing**: File validation and size limits (16MB)
- **� Real-time Monitoring**: Processing statistics and performance metrics
- **�️ Error Handling**: Comprehensive error management and user feedback

## 🛠️ Technology Stack

### 🌐 **Web Application** (Live at https://summabrowser-api.onrender.com)
- **Flask**: Production web server with CORS support
- **HTML5/CSS3**: Modern responsive web interface
- **JavaScript ES6+**: Async/await, Fetch API, modern DOM manipulation
- **Online OCR**: OCR.space API integration for image processing
- **Render Deployment**: Production hosting with automatic deployments

### 🔌 **Browser Extension**
- **Manifest V3**: Latest Chrome extension architecture
- **Modern CSS**: CSS Grid, Flexbox, CSS Variables, and animations
- **Vanilla JavaScript**: ES6+ with async/await and Chrome APIs
- **Font Awesome**: Beautiful icons and visual elements

### 🤖 **AI & Processing Backend**
- **Flask**: Lightweight web framework with API endpoints
- **PyPDF2**: Advanced PDF text extraction
- **Pillow (PIL)**: Image processing and manipulation
- **Custom NLP**: Advanced text summarization with sentence scoring
- **Online OCR**: OCR.space integration for reliable text extraction

### ☁️ **Production Infrastructure**
- **Render.com**: Free tier hosting with automatic deployments
- **GitHub Integration**: Continuous deployment from repository
- **Environment Variables**: Secure API key management
- **Health Monitoring**: API status and uptime tracking

## 🚀 Quick Start

### Option 1: Use the Live Web App (Recommended)
1. **Visit:** https://summabrowser-api.onrender.com
2. **Upload:** Drag and drop your PDF or image file
3. **Process:** Click "Generate AI Summary"
4. **Get Results:** View, copy, or download your summary

### Option 2: Install Browser Extension
1. **Download:** Clone this repository or download the ZIP
2. **Load Extension:** Go to `chrome://extensions/` → Enable Developer Mode → Load Unpacked
3. **Select Folder:** Choose the `SummaBrowse` directory
4. **Use:** Click the extension icon and start processing documents

### Option 3: Run Locally
```bash
# Clone the repository
git clone https://github.com/eepanshu/Summa_Browser.git
cd Summa_Browser/SummaBrowse

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-cors requests Pillow PyPDF2

# Run the application
python app-web.py
```

## 🚀 Usage

### 🌐 **Web Application** (https://summabrowser-api.onrender.com)
1. **Visit the Live App**: Open https://summabrowser-api.onrender.com in any modern browser
2. **Upload Document**: 
   - Drag and drop a file onto the upload area, or
   - Click the upload area to browse and select a document
3. **File Validation**: System automatically validates file type and size
4. **Process Document**: Click "Generate AI Summary" to start processing
5. **Real-time Progress**: Watch the progress bar and status updates
6. **Get Results**: 
   - View summary preview in the interface
   - See processing statistics (compression ratio, word counts)
   - Download complete summary as text file
   - Copy summary to clipboard with one click

### 🔌 **Browser Extension**
1. **Load Extension**: Install from Chrome Web Store or load unpacked
2. **Click Icon**: Click the SummaBrowser icon in your browser toolbar
3. **Upload File**: Use the same drag-and-drop or browse functionality
4. **Connected Processing**: Extension connects to live API for processing
5. **Seamless Integration**: Process documents without leaving your current page

### 📱 **Mobile & Tablet**
The web interface is fully responsive and works perfectly on:
- 📱 **Mobile phones** - Optimized touch interface
- 📊 **Tablets** - Full feature support
- 💻 **Desktop** - Complete functionality

## 🎯 Supported File Types & Limits

### ✅ **Supported Formats**
- **📄 Documents**: `.pdf`, `.txt`
- **🖼️ Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`
- **📏 File Size**: Up to 16MB per file
- **📚 Content**: Multi-page PDFs, complex layouts, images with text

### ⚡ **Performance Expectations**
- **📄 Small PDFs (1-5 pages)**: 15-30 seconds
- **📚 Large PDFs (10+ pages)**: 30-60 seconds
- **🖼️ Images with OCR**: 20-45 seconds
- **📝 Text files**: 5-15 seconds

## 🔗 **Live API Endpoints**

Base URL: `https://summabrowser-api.onrender.com`

- **🏠 Web Interface**: `GET /` - Beautiful HTML interface
- **💓 Health Check**: `GET /health` - API status and services
- **🔄 Process Document**: `POST /process` - Upload and process files
- **📥 Download**: `GET /download/<filename>` - Download processed summaries

### **API Usage Example**
```bash
# Health check
curl https://summabrowser-api.onrender.com/health

# Process a document
curl -X POST -F "file=@document.pdf" https://summabrowser-api.onrender.com/process

# Response includes summary, download URL, and processing stats
```

## 📁 Project Structure

```
SummaBrowse/
├── 🌐 Web Interface Files
│   ├── app-web.py              # Complete web app with HTML interface
│   ├── test-your-api.html      # Local API testing interface
│   ├── deployment-monitor.html # Deployment status monitor
│   └── RENDER_UPDATE.md        # Deployment guide
│
├── 🔌 Browser Extension
│   ├── manifest.json           # Extension configuration (Manifest V3)
│   ├── popup.html             # Extension popup interface
│   ├── popup.js               # Frontend JavaScript logic
│   ├── styles.css             # Modern CSS styling with themes
│   ├── background.js          # Service worker script
│   └── icons/                 # Extension icons (16px to 128px)
│
├── ☁️ Production Backend
│   ├── summary/
│   │   ├── app-web.py         # Production Flask app with web UI
│   │   ├── app-ocr.py         # API-only version
│   │   ├── requirements-ocr.txt # Production dependencies
│   │   ├── uploads/           # Temporary file storage
│   │   └── output/            # Generated summaries
│
├── 🚀 Deployment
│   ├── render.yaml            # Render.com deployment config
│   ├── DEPLOYMENT.md          # Deployment documentation
│   └── .gitignore            # Git ignore rules
│
└── 📚 Documentation
    ├── README.md              # This comprehensive guide
    ├── TESTING_GUIDE.md       # Complete testing instructions
    └── test-document.txt      # Sample file for testing
```

## ⚙️ Configuration & Customization

### 🌐 **Live Web App Configuration**
The production app at https://summabrowser-api.onrender.com is pre-configured with:
- **OCR API**: OCR.space free tier integration
- **File Limits**: 16MB maximum upload size
- **Processing**: Advanced AI summarization algorithm
- **CORS**: Enabled for cross-origin requests
- **Environment**: Production-optimized with error handling

### 🔌 **Browser Extension Configuration**
Configure the extension to use different APIs:

```javascript
// In popup.js, modify the API endpoint:
this.API_BASE_URL = 'https://summabrowser-api.onrender.com'; // Live API
// or
this.API_BASE_URL = 'http://localhost:5000'; // Local development
```

### 🎨 **UI Customization**
Customize the interface appearance:

```css
/* In styles.css, modify CSS variables */
:root {
  --primary-color: #3498db;      /* Main theme color */
  --success-color: #27ae60;      /* Success messages */
  --error-color: #e74c3c;        /* Error messages */
  --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### 🔧 **API Configuration**
For local development or custom deployment:

```python
# In app-web.py, modify settings:
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # File size limit
OCR_API_KEY = os.environ.get('OCR_API_KEY', 'helloworld')  # OCR service
PORT = int(os.environ.get('PORT', 5000))  # Server port
```

## 🔧 Development & Contributing

### 🚀 **Local Development Setup**
```bash
# Clone the repository
git clone https://github.com/eepanshu/Summa_Browser.git
cd Summa_Browser/SummaBrowse

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install flask flask-cors requests Pillow PyPDF2

# Run in development mode
python app-web.py
# App runs at http://localhost:5000 with debug mode

# Load browser extension in development
# Go to chrome://extensions/ → Developer mode → Load unpacked
```

### 🧪 **Testing**
```bash
# Test the live API
curl https://summabrowser-api.onrender.com/health

# Test local development
curl http://localhost:5000/health

# Use provided testing tools
open test-your-api.html  # Web interface tester
open deployment-monitor.html  # Deployment monitor
```

### 🔄 **Deployment Process**
The app uses automatic deployment via Render.com:

1. **Push to GitHub**: `git push origin main`
2. **Automatic Build**: Render detects changes and builds
3. **Live Deployment**: Updates at https://summabrowser-api.onrender.com
4. **Health Check**: Automatic verification and rollback if needed

### 🤝 **Contributing Guidelines**
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Test** your changes with both web interface and browser extension
4. **Commit** with clear messages: `git commit -m 'Add amazing feature'`
5. **Push** to your branch: `git push origin feature/amazing-feature`
6. **Create** a Pull Request with detailed description

### 🏗️ **Architecture Overview**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │ Browser Extension│    │   Mobile/Tablet │
│  (Any Device)   │    │ (Chrome/Edge)   │    │   Web Browser   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
          ┌─────────────────────────────────────────────────────┐
          │         Live API Server (Render.com)                │
          │    https://summabrowser-api.onrender.com           │
          │                                                     │
          │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
          │  │   Flask     │  │    OCR      │  │     AI      │ │
          │  │ Web Server  │  │  Service    │  │Summarization│ │
          │  └─────────────┘  └─────────────┘  └─────────────┘ │
          └─────────────────────────────────────────────────────┘
```

## 🐛 Troubleshooting & Support

### 🌐 **Web Interface Issues**
**Can't access the web app:**
- ✅ Check URL: https://summabrowser-api.onrender.com
- ✅ Wait 30 seconds (Render free tier may have cold starts)
- ✅ Try refreshing the page
- ✅ Check https://status.render.com for service status

**File upload not working:**
- ✅ Verify file size is under 16MB
- ✅ Check file format (PDF, PNG, JPG, TXT supported)
- ✅ Ensure stable internet connection
- ✅ Try a different browser or clear cache

**Processing stuck or fails:**
- ✅ Check file isn't corrupted or password-protected
- ✅ Try with a simpler test document
- ✅ Check browser console (F12) for error messages
- ✅ Refresh page and try again

### 🔌 **Browser Extension Issues**
**Extension not loading:**
- ✅ Verify Chrome Developer Mode is enabled
- ✅ Check manifest.json is valid (no syntax errors)
- ✅ Ensure all required files are present
- ✅ Try removing and re-adding the extension

**API connection failed:**
- ✅ Check internet connection
- ✅ Verify API URL in popup.js is correct
- ✅ Check if https://summabrowser-api.onrender.com/health returns success
- ✅ Try switching to web interface as alternative

### 🛠️ **Development Issues**
**Local server won't start:**
- ✅ Verify Python 3.8+ is installed
- ✅ Check all dependencies are installed: `pip install -r requirements-ocr.txt`
- ✅ Ensure port 5000 isn't already in use
- ✅ Check for error messages in terminal

**OCR not extracting text:**
- ✅ Verify image quality and resolution (higher is better)
- ✅ Check if image contains clear, readable text
- ✅ Try different image formats (PNG often works best)
- ✅ Ensure OCR API key is valid

### 📞 **Get Help**
If issues persist:

1. **📋 Check Issues**: [GitHub Issues](https://github.com/eepanshu/Summa_Browser/issues)
2. **🆕 Create Issue**: Include:
   - Operating system and browser version
   - Error messages or screenshots
   - Steps to reproduce the problem
   - File type and size being processed
3. **💡 Feature Requests**: Use the same issue tracker
4. **📧 Direct Contact**: For urgent issues or private concerns

## 🎯 Performance & Optimization

### ⚡ **Speed Optimization**
- **🌐 CDN Integration**: Static assets served via CDN
- **📦 File Compression**: Automatic compression for faster uploads
- **🔄 Async Processing**: Non-blocking file processing
- **💾 Smart Caching**: Intelligent caching for repeated operations

### 📊 **Monitoring & Analytics**
- **📈 Health Checks**: Automatic API health monitoring
- **⏱️ Performance Metrics**: Processing time tracking
- **📋 Error Logging**: Comprehensive error tracking and reporting
- **💯 Uptime Monitoring**: 24/7 service availability tracking

### 🎨 **UI/UX Optimization**
- **📱 Responsive Design**: Optimized for all screen sizes
- **🎭 Smooth Animations**: Hardware-accelerated CSS animations
- **♿ Accessibility**: ARIA labels and keyboard navigation support
- **🌓 Theme Support**: System preference detection for dark/light mode

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

## 🔮 Roadmap & Future Features

### 🎯 **Phase 1: Enhanced AI Capabilities**
- [ ] **🤖 Multiple AI Models**: Integration with GPT, Claude, and other AI services
- [ ] **📏 Custom Summary Lengths**: User-defined summary sizes (short, medium, long)
- [ ] **🎨 Summary Styles**: Academic, business, casual, technical writing styles
- [ ] **🔍 Key Information Extraction**: Automatic extraction of dates, names, numbers
- [ ] **📊 Content Analysis**: Sentiment analysis, topic classification

### 🎯 **Phase 2: Advanced Features**
- [ ] **🌍 Multi-language Support**: Process documents in 50+ languages
- [ ] **📁 Batch Processing**: Upload and process multiple files simultaneously
- [ ] **📚 Document History**: Save and search through processed documents
- [ ] **🔗 Cloud Integration**: Google Drive, Dropbox, OneDrive support
- [ ] **📱 Mobile Apps**: Native iOS and Android applications

### 🎯 **Phase 3: Enterprise Features**
- [ ] **👥 Team Collaboration**: Share summaries and collaborate on documents
- [ ] **🔐 Advanced Security**: End-to-end encryption, SSO integration
- [ ] **📈 Analytics Dashboard**: Usage statistics and insights
- [ ] **🔌 API Integration**: RESTful API for third-party integrations
- [ ] **⚡ Premium Processing**: Faster processing with dedicated resources

### 🎯 **Phase 4: Export & Integration**
- [ ] **📄 Export Formats**: PDF, DOCX, HTML, Markdown export options
- [ ] **🔗 Browser Integration**: Right-click context menu integration
- [ ] **📧 Email Integration**: Direct email sharing of summaries
- [ ] **💼 Business Tools**: Slack, Teams, Notion integration
- [ ] **🎓 Educational Tools**: Canvas, Blackboard, Moodle integration

## 📄 License & Legal

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### 🛡️ **Privacy & Security**
- **🔒 No Data Storage**: Files are processed and immediately deleted
- **🌐 Secure Transmission**: All data transferred over HTTPS
- **🔑 API Keys**: Securely managed environment variables
- **📋 Compliance**: GDPR and CCPA compliant processing

### ⚖️ **Terms of Use**
- **✅ Free for Personal Use**: Individual and educational use encouraged
- **💼 Commercial Use**: Allowed under MIT license terms
- **🔄 Modification**: Free to modify and distribute
- **📞 Attribution**: Credit appreciated but not required

## 🤝 Contributing & Community

### 🌟 **Ways to Contribute**
- **🐛 Bug Reports**: Help us find and fix issues
- **💡 Feature Requests**: Suggest new functionality
- **📝 Documentation**: Improve guides and tutorials
- **🌍 Translations**: Help localize the interface
- **💻 Code Contributions**: Submit pull requests

### 🏆 **Contributors**
Special thanks to all contributors who help make SummaBrowser better:

<div align="center">
  <p><em>🌟 Star this repository to show your support!</em></p>
  <p><em>🍴 Fork it to start contributing!</em></p>
  <p><em>📣 Share it with your friends and colleagues!</em></p>
</div>

### 📞 **Community & Support**
- **💬 Discussions**: [GitHub Discussions](https://github.com/eepanshu/Summa_Browser/discussions)
- **🐛 Issues**: [GitHub Issues](https://github.com/eepanshu/Summa_Browser/issues)
- **📧 Contact**: Open an issue for questions and support
- **🌐 Live Demo**: https://summabrowser-api.onrender.com

## 🙏 Acknowledgments & Credits

### 🛠️ **Technology Partners**
- **[Render.com](https://render.com)** - Reliable cloud hosting platform
- **[OCR.space](https://ocr.space)** - Powerful OCR API service
- **[Flask](https://flask.palletsprojects.com/)** - Lightweight Python web framework
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF processing library

### 🎨 **Design & UI**
- **[Font Awesome](https://fontawesome.com/)** - Beautiful icon library
- **[Google Fonts](https://fonts.google.com/)** - Web typography
- **[CSS Gradient](https://cssgradient.io/)** - Beautiful gradient generator
- **[Unsplash](https://unsplash.com/)** - High-quality images and inspiration

### 🤖 **AI & Processing**
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Image processing capabilities
- **[Requests](https://requests.readthedocs.io/)** - HTTP library for API integration
- **Modern Web Standards** - HTML5, CSS3, ES6+ JavaScript

---

<div align="center">
  <h2>🚀 Ready to Get Started?</h2>
  
  <p>
    <a href="https://summabrowser-api.onrender.com" target="_blank">
      <img src="https://img.shields.io/badge/🌐%20Try%20Live%20Demo-summabrowser--api.onrender.com-success?style=for-the-badge" alt="Try Live Demo">
    </a>
  </p>
  
  <p>
    <a href="https://github.com/eepanshu/Summa_Browser/fork" target="_blank">
      <img src="https://img.shields.io/badge/🍴%20Fork%20Repository-Contribute%20Now-blue?style=for-the-badge&logo=github" alt="Fork Repository">
    </a>
  </p>
  
  <br>
  
  <p><strong>⭐ Star this repository if SummaBrowser helped you!</strong></p>
  <p><em>Made with ❤️ by the SummaBrowser Team</em></p>
  <p><em>🌟 Turning documents into insights, one summary at a time</em></p>
</div>
