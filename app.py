import os
import argostranslate.package
import argostranslate.translate
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global translator variable
translator = None


def download_and_install_model():
    """
    Download and install the English to Hebrew translation model if not already installed.
    """
    print("Checking for English to Hebrew translation model...")
    
    # Update package index
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    
    # Find English to Hebrew package
    en_he_package = None
    for package in available_packages:
        if package.from_code == "en" and package.to_code == "he":
            en_he_package = package
            break
    
    if en_he_package is None:
        raise Exception("English to Hebrew translation package not found in Argos Translate repository")
    
    # Check if already installed
    installed_packages = argostranslate.package.get_installed_packages()
    is_installed = any(
        pkg.from_code == "en" and pkg.to_code == "he" 
        for pkg in installed_packages
    )
    
    if not is_installed:
        print(f"Downloading and installing English to Hebrew model...")
        argostranslate.package.install_from_path(en_he_package.download())
        print("Model installation complete!")
    else:
        print("English to Hebrew model already installed.")


def initialize_translator():
    """
    Initialize the translator object.
    """
    global translator
    
    # Download model if needed
    download_and_install_model()
    
    # Get the installed translation
    installed_languages = argostranslate.translate.get_installed_languages()
    
    # Find English language
    en_lang = None
    for lang in installed_languages:
        if lang.code == "en":
            en_lang = lang
            break
    
    if en_lang is None:
        raise Exception("English language not found in installed packages")
    
    # Get Hebrew translation from English
    translator = en_lang.get_translation(argostranslate.translate.Language("he", "Hebrew"))
    
    if translator is None:
        raise Exception("English to Hebrew translator not found")
    
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
        
        # Translate the text
        translation = translator.translate(text)
        
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
    
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)  # debug=False in production

