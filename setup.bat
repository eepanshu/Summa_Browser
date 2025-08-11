@echo off
REM SummaBrowser Setup Script for Windows
echo 🚀 Setting up SummaBrowser...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📚 Installing Python dependencies...
cd summary
pip install -r requirements.txt

REM Check if Tesseract is installed
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Tesseract OCR is not installed.
    echo Please download and install Tesseract from:
    echo https://github.com/tesseract-ocr/tesseract/releases
) else (
    echo ✅ Tesseract OCR found
)

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "output" mkdir output

cd ..

echo 🎉 Setup complete!
echo.
echo Next steps:
echo   1. Install Tesseract OCR if not already installed
echo   2. Load the extension in Chrome:
echo      - Open chrome://extensions/
echo      - Enable Developer mode
echo      - Click 'Load unpacked' and select the SummaBrowse folder
echo   3. Start the backend server:
echo      cd summary ^&^& python app.py
echo.
echo 🚀 SummaBrowser is ready to use!
pause
