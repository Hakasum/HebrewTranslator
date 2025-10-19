# Hebrew Translator API

A local REST API for translating English text to Hebrew using HuggingFace Transformers with the Helsinki-NLP MarianMT model. The API uses Flask and provides a simple POST endpoint for translation requests.

## Features

- 🌐 Local translation API (no cloud dependencies after initial setup)
- 🚀 Fast startup with automatic model download
- 🐳 Docker support for easy deployment
- 💪 Works offline after initial model download
- ✅ Simple JSON-based API

## Requirements

- Python 3.11+ (for local installation)
- Docker (for containerized deployment)
- **Minimum 1GB RAM** for running the translation model

> ⚠️ **Note:** Free-tier hosting services with 512MB RAM (like Render free tier) may run out of memory. See [DEPLOYMENT.md](DEPLOYMENT.md) for hosting recommendations.

## Installation

### Option 1: Local Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

On first run, the application will automatically download the English to Hebrew translation model (~40MB). This may take a minute depending on your internet connection.

The API will start on `http://localhost:5005`

### Option 2: Docker

1. Build the Docker image:
```bash
docker build -t hebrew-translator .
```

2. Run the container:
```bash
docker run -p 5005:5005 hebrew-translator
```

On first run, the model will be downloaded inside the container. To persist the model across container restarts, you can mount a volume:

```bash
docker run -p 5005:5005 -v hebrew-translator-data:/root/.cache/huggingface hebrew-translator
```

## API Usage

### Translate Endpoint

**POST** `/translate`

Translates English text to Hebrew.

**Request:**
```json
{
  "text": "Hello world"
}
```

**Response:**
```json
{
  "translation": "שלום עולם"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:5005/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

**Example with Python:**
```python
import requests

response = requests.post(
    "http://localhost:5005/translate",
    json={"text": "Hello world"}
)

print(response.json())
# Output: {'translation': 'שלום עולם'}
```

### Health Check Endpoint

**GET** `/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "Hebrew Translator API"
}
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad request (missing or invalid parameters)
- `500` - Server error (translation failed)

**Error Response Format:**
```json
{
  "error": "Error message description"
}
```

## Offline Usage

After the initial model download, the API works completely offline. The translation model is cached locally by HuggingFace in:

- **Linux/Mac:** `~/.cache/huggingface/hub/`
- **Windows:** `%USERPROFILE%\.cache\huggingface\hub\`
- **Docker:** Inside the container at `/root/.cache/huggingface/hub/`

## Technical Details

- **Framework:** Flask 3.0.0
- **Translation Engine:** HuggingFace Transformers 4.36.0
- **Model:** Helsinki-NLP/opus-mt-en-he (MarianMT)
- **Port:** 5005 (configurable via PORT environment variable)

## License

This project uses HuggingFace Transformers and Helsinki-NLP models, which are open-source and free to use. The MarianMT models are from the OPUS-MT project.

