#!/bin/bash

# SummaBrowser Setup Script
echo "🚀 Setting up SummaBrowser..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed. Please install pip.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 found${NC}"

# Create virtual environment
echo -e "${BLUE}📦 Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies
echo -e "${BLUE}📚 Installing Python dependencies...${NC}"
cd summary
pip install -r requirements.txt

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo -e "${YELLOW}⚠️  Tesseract OCR is not installed.${NC}"
    echo -e "${BLUE}Please install Tesseract:${NC}"
    echo -e "  ${BLUE}Ubuntu/Debian:${NC} sudo apt-get install tesseract-ocr"
    echo -e "  ${BLUE}macOS:${NC} brew install tesseract"
    echo -e "  ${BLUE}Windows:${NC} Download from https://github.com/tesseract-ocr/tesseract/releases"
else
    echo -e "${GREEN}✅ Tesseract OCR found${NC}"
fi

# Create necessary directories
mkdir -p uploads output

cd ..

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Install Tesseract OCR if not already installed"
echo -e "  2. Load the extension in Chrome:"
echo -e "     - Open chrome://extensions/"
echo -e "     - Enable Developer mode"
echo -e "     - Click 'Load unpacked' and select the SummaBrowse folder"
echo -e "  3. Start the backend server:"
echo -e "     ${YELLOW}cd summary && python app.py${NC}"

echo -e "${GREEN}🚀 SummaBrowser is ready to use!${NC}"
