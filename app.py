import os
import gc
import time
import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global model and tokenizer (M2M-100 supports 100 languages in one model)
model = None
tokenizer = None

# Model name - Facebook M2M-100 (418M is the smallest variant)
MODEL_NAME = "facebook/m2m100_418M"

# Default languages
DEFAULT_SOURCE = "en"
DEFAULT_TARGET = "he"

# Supported languages
SUPPORTED_LANGS = {
    "en": "English",
    "es": "Spanish", 
    "de": "German",
    "he": "Hebrew"
}


def initialize_translator() -> None:
    """
    Initialize the M2M-100 multilingual translation model.
    Downloads on first run and caches locally.
    Supports direct translation between 100 languages including en/es/de -> he.
    """
    global model, tokenizer
    
    print("="*60)
    print("[Model] Loading M2M-100 Multilingual Translation Model")
    print("="*60)
    print(f"[Model] Model: {MODEL_NAME}")
    print(f"[Model] Supported languages:")
    for code, name in SUPPORTED_LANGS.items():
        print(f"         - {code}: {name}")
    print("[Model] Downloading model (first run only, ~1.6GB)...")
    
    # Load tokenizer and model with memory optimizations
    tokenizer = M2M100Tokenizer.from_pretrained(MODEL_NAME)
    model = M2M100ForConditionalGeneration.from_pretrained(
        MODEL_NAME,
        low_cpu_mem_usage=True,
        torch_dtype="auto"
    )
    model.eval()
    
    print("[Model] ✓ Model loaded successfully!")
    print("="*60 + "\n")


@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate text between supported languages.
    
    Request JSON:
    {
        "text": "Hello world",
        "source": "en",  # Optional, defaults to "en"
        "target": "he"   # Optional, defaults to "he"
    }
    
    Response JSON:
    {
        "translation": "שלום עולם",
        "source": "en",
        "target": "he",
        "time_seconds": 1.234
    }
    
    Supported languages: en (English), es (Spanish), de (German), he (Hebrew)
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        if "text" not in data:
            return jsonify({"error": "Missing 'text' field in JSON payload"}), 400
        
        text = data["text"]
        source_lang = (data.get("source") or DEFAULT_SOURCE).strip().lower()
        target_lang = (data.get("target") or DEFAULT_TARGET).strip().lower()
        
        if not isinstance(text, str):
            return jsonify({"error": "'text' field must be a string"}), 400
        
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Validate language codes
        if source_lang not in SUPPORTED_LANGS:
            return jsonify({
                "error": f"Unsupported source language: '{source_lang}'",
                "supported": list(SUPPORTED_LANGS.keys())
            }), 400
        
        if target_lang not in SUPPORTED_LANGS:
            return jsonify({
                "error": f"Unsupported target language: '{target_lang}'",
                "supported": list(SUPPORTED_LANGS.keys())
            }), 400
        
        # Log request
        print(f"\n[Request] Translation request received")
        print(f"[Request] {source_lang} -> {target_lang}")
        print(f"[Request] Text length: {len(text)} chars")
        print(f"[Request] Input: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        t_start = time.time()
        
        # Translate using M2M-100
        with torch.no_grad():  # Disable gradient calculation to save memory
            # Set source language
            tokenizer.src_lang = source_lang
            
            # Tokenize input
            t0 = time.time()
            inputs = tokenizer(text, return_tensors="pt", padding=True)
            t1 = time.time()
            
            # Generate translation with forced target language
            generated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.get_lang_id(target_lang),
                max_length=512
            )
            t2 = time.time()
            
            # Decode translation
            translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            t3 = time.time()
        
        t_total = time.time() - t_start
        
        # Log timing
        print(f"[Timing] Tokenize: {t1 - t0:.3f}s")
        print(f"[Timing] Generate: {t2 - t1:.3f}s")
        print(f"[Timing] Decode: {t3 - t2:.3f}s")
        print(f"[Timing] Total: {t_total:.3f}s")
        print(f"[Result] Output: {translation}")
        print("-" * 60)
        
        # Clean up
        del inputs, generated_tokens
        gc.collect()
        
        return jsonify({
            "translation": translation,
            "source": source_lang,
            "target": target_lang,
            "time_seconds": round(t_total, 3)
        }), 200
    
    except Exception as e:
        print(f"[Error] Translation failed: {str(e)}")
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "healthy",
        "service": "Multilingual Hebrew Translator API",
        "model": MODEL_NAME,
        "supported_languages": SUPPORTED_LANGS
    }), 200


@app.route('/languages', methods=['GET'])
def languages():
    """
    Get list of supported languages.
    """
    return jsonify({
        "supported_languages": SUPPORTED_LANGS
    }), 200


if __name__ == '__main__':
    # Initialize translator on startup
    print("\n" + "="*60)
    print("Starting Multilingual Hebrew Translator API")
    print("="*60 + "\n")
    
    initialize_translator()
    
    port = int(os.environ.get('PORT', 5005))
    print(f"[Server] Starting Flask server on port {port}...")
    print(f"[Server] API ready at http://localhost:{port}")
    print(f"[Server] Endpoints:")
    print(f"         - POST /translate  (translate text)")
    print(f"         - GET  /health     (health check)")
    print(f"         - GET  /languages  (list supported languages)")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
