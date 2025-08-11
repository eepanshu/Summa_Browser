import os
# Set PyDev debugger timeout to a higher value
os.environ['PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT'] = '2.0'

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from text_extraction_and_summarization import TextExtractorAndSummarizer
from process_pdf import PDFProcessor
import logging
from datetime import datetime

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
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('summabrowser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'SummaBrowser Backend Running',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'ocr': 'available',
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
            summarizer = TextExtractorAndSummarizer()
            text = summarizer.extract_text_from_image(file_path)
            if text:
                summary = summarizer.generate_summary(text)
            else:
                logger.error('Failed to extract text from image')
                
        elif file_ext.lower() == '.pdf':
            # Process PDF
            logger.info('Processing PDF file')
            processor = PDFProcessor()
            text = processor.extract_text_with_ocr(file_path)
            if text:
                summary = processor.summarize_text(text)
            else:
                logger.error('Failed to extract text from PDF')

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
    logger.info('Starting SummaBrowser Backend Server')
    logger.info(f'Upload folder: {app.config["UPLOAD_FOLDER"]}')
    logger.info(f'Output folder: {OUTPUT_FOLDER}')
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    app.run(debug=True)