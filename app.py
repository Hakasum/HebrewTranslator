import os
from transformers import MarianMTModel, MarianTokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global model and tokenizer variables
model = None
tokenizer = None

# Model name for English to Hebrew translation
MODEL_NAME = "Helsinki-NLP/opus-mt-en-he"


def initialize_translator():
    """
    Initialize the translation model and tokenizer.
    Downloads the model on first run if not already cached.
    """
    global model, tokenizer
    
    print("Loading English to Hebrew translation model...")
    print(f"Model: {MODEL_NAME}")
    
    # Load tokenizer and model
    # These will be downloaded on first run and cached locally
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)
    
    print("Translator initialized successfully!")


@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate English text to Hebrew.
    Expects JSON payload: { "text": "Hello world" }
    Returns: { "translation": "שלום עולם" }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        if "text" not in data:
            return jsonify({"error": "Missing 'text' field in JSON payload"}), 400
        
        text = data["text"]
        
        if not isinstance(text, str):
            return jsonify({"error": "'text' field must be a string"}), 400
        
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Tokenize and translate the text
        inputs = tokenizer([text], return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        translation = tokenizer.decode(translated[0], skip_special_tokens=True)
        
        return jsonify({"translation": translation}), 200
    
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({"status": "healthy", "service": "Hebrew Translator API"}), 200


if __name__ == '__main__':
    # Initialize translator on startup
    print("Starting Hebrew Translator API...")
    initialize_translator()
    
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=False)

