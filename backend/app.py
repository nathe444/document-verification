from flask import Flask, request, jsonify
from flask_cors import CORS
from document_processor import DocumentProcessor
from openai_handler import OpenAIHandler
import os
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
app.logger.setLevel(logging.ERROR)

doc_processor = DocumentProcessor()
ai_handler = OpenAIHandler()

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({
            "status": "error", 
            "message": "No selected file"
        }), 400
    
    # Get analysis type from form data or query parameters
    analysis_type = request.form.get('analysis_type') or request.args.get('analysis_type', 'factual_accuracy_verification')
    
    try:
        # Extract text from document
        extracted_text = doc_processor.extract_text(file)
        
        # Process with OpenAI
        analysis_result = ai_handler.process_document(
            text=extracted_text, 
            prompt_type=analysis_type
        )
        
        return jsonify({
            "status": "success",
            "original_text": extracted_text,
            "analysis": analysis_result,
            "filename": file.filename,
            "analysis_type": analysis_type
        })
    
    except Exception as e:
        app.logger.error(f"Error processing document: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}",
            "details": {
                "analysis_type": analysis_type,
                "filename": file.filename
            }
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)