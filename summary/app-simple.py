import os
# Set PyDev debugger timeout to a higher value
os.environ['PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT'] = '2.0'

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
from datetime import datetime
import tempfile
import shutil

# Simplified imports without heavy dependencies
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def simple_summarize(text, max_sentences=3):
    """Simple text summarization without external dependencies"""
    if not text or len(text.strip()) < 50:
        return "Text is too short to summarize effectively."
    
    # Split into sentences
    sentences = text.replace('\n', ' ').split('. ')
    sentences = [s.strip() + '.' for s in sentences if len(s.strip()) > 10]
    
    if len(sentences) <= max_sentences:
        return ' '.join(sentences)
    
    # Take first, middle, and last sentences for a basic summary
    if len(sentences) >= 3:
        summary_sentences = [
            sentences[0],
            sentences[len(sentences)//2],
            sentences[-1]
        ]
    else:
        summary_sentences = sentences[:max_sentences]
    
    return ' '.join(summary_sentences)

def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR"""
    if not OCR_AVAILABLE:
        return "OCR functionality not available. Please install required dependencies."
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        return None

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'SummaBrowser Backend Running',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'ocr_available': OCR_AVAILABLE
    })

@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'ocr': 'available' if OCR_AVAILABLE else 'limited',
            'summarization': 'available',
            'file_processing': 'available'
        }
    })

@app.route('/process', methods=['POST'])
def process_file():
    """Process uploaded file and generate summary"""
    try:
        # Validate request
        if 'file' not in request.files:
            logger.warning('No file in request')
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            logger.warning('Empty filename')
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        file_ext = os.path.splitext(file.filename.lower())[1]
        if file_ext not in allowed_extensions:
            logger.warning(f'Invalid file type: {file_ext}')
            return jsonify({'error': 'Unsupported file type. Please upload a PDF or image file.'}), 400

        # Process filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure unique filename
        if os.path.exists(file_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(file_path):
                filename = f"{base}_{counter}{ext}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                counter += 1

        # Save uploaded file
        file.save(file_path)
        logger.info(f'File saved: {filename}')

        # Process based on file type
        text = None
        summary = None

        if file_ext.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}:
            # Process image
            logger.info('Processing image file')
            text = extract_text_from_image(file_path)
            if text and len(text.strip()) > 10:
                summary = simple_summarize(text)
            else:
                text = "Could not extract readable text from the image."
                summary = "Unable to generate summary - no readable text found in the image."
                
        elif file_ext.lower() == '.pdf':
            # For PDF, provide a placeholder response since PyPDF2 isn't included
            text = "PDF processing requires additional setup. Please use image files for now."
            summary = "PDF processing is not available in this deployment. Please convert your PDF to an image format and try again."

        # Validate results
        if not text or text.strip() == '':
            logger.error('No text extracted from file')
            return jsonify({'error': 'Could not extract text from the file. Please ensure the file contains readable text.'}), 500
            
        if not summary or summary.strip() == '':
            logger.error('No summary generated')
            return jsonify({'error': 'Could not generate summary. The extracted text may be too short or unclear.'}), 500

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save extracted text
        extracted_text_file = os.path.join(OUTPUT_FOLDER, f"extracted_text_{timestamp}.txt")
        with open(extracted_text_file, 'w', encoding='utf-8') as f:
            f.write(text)

        # Save summary
        summary_file = os.path.join(OUTPUT_FOLDER, f"summary_{timestamp}.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)

        logger.info(f'Processing completed successfully for {filename}')

        return jsonify({
            'success': True,
            'extracted_text': text[:500] + '...' if len(text) > 500 else text,  # Truncate for response
            'summary': summary,
            'download_url': f'/download/summary_{timestamp}.txt',
            'file_info': {
                'name': filename,
                'size': os.path.getsize(file_path),
                'type': file_ext
            }
        })

    except Exception as e:
        logger.error(f'Error processing file: {str(e)}', exc_info=True)
        return jsonify({
            'error': f'An error occurred while processing the file: {str(e)}'
        }), 500

    finally:
        # Clean up uploaded file to save space
        try:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f'Cleaned up uploaded file: {filename}')
        except Exception as e:
            logger.warning(f'Could not clean up file {filename}: {str(e)}')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated summary file"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            logger.info(f'File downloaded: {filename}')
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            logger.error(f'File not found: {filename}')
            return jsonify({'error': f'File {filename} not found'}), 404
    except Exception as e:
        logger.error(f'Error downloading file {filename}: {str(e)}')
        return jsonify({'error': 'An error occurred while downloading the file'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size allowed is 16MB.'}), 413

@app.errorhandler(500)
def internal_server_error(e):
    """Handle internal server errors"""
    logger.error(f'Internal server error: {str(e)}')
    return jsonify({'error': 'Internal server error. Please try again later.'}), 500

if __name__ == '__main__':
    import os
    logger.info('Starting SummaBrowser Backend Server')
    logger.info(f'Upload folder: {app.config["UPLOAD_FOLDER"]}')
    logger.info(f'Output folder: {OUTPUT_FOLDER}')
    logger.info(f'OCR Available: {OCR_AVAILABLE}')
    
    # Get port from environment variable (for deployment) or use default
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    debug = 'PORT' not in os.environ  # Debug only in local development
    
    app.run(debug=debug, host=host, port=port)
