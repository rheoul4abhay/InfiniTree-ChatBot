from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from datetime import datetime

from llm_client import query_gemini, build_prompt
from file_processor import extract_text_from_file  # file text reader

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/generate', methods=['POST', 'PUT'])
def generate_response():
    start_time = datetime.now()
    logger.info("Generate request started")
    
    try:
        # Parse request data
        is_json = request.method == 'PUT' and request.is_json
        data_source = request.get_json() if is_json else request.form
        
        prompt = data_source.get('prompt', '').strip()
        temperature = float(data_source.get('temperature', 0.7))
        top_p = float(data_source.get('top_p', 0.9))
        top_k = int(data_source.get('top_k', 40))
        file = None if is_json else request.files.get('context_file')
            
        # Validate inputs
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        if not all([0 <= temperature <= 1, 0 <= top_p <= 1, 1 <= top_k <= 100]):
            return jsonify({"error": "Invalid parameter ranges"}), 400

        # Process file if present
        file_text = ""
        filepath = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(tempfile.gettempdir(), filename)
            file.save(filepath)
            file_text = extract_text_from_file(filepath)
            logger.info(f"Processed file: {file.filename}")

        # Generate response
        full_prompt = build_prompt(prompt, file_text)
        response = query_gemini(full_prompt, temperature, top_p, top_k)
        
        # Cleanup temp file
        if filepath:
            try:
                os.remove(filepath)
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Request completed in {duration:.2f}s")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting GenAI ChatBot API")
    app.run(host='0.0.0.0', port=5000, debug=True)