# Deployment Guide

## Memory Requirements

The Helsinki-NLP MarianMT model with PyTorch requires approximately **1GB of RAM** to run comfortably. This project includes memory optimizations, but free-tier hosting with 512MB RAM will likely still struggle.

## Deployment Options

### Option 1: Render - Starter Plan (Recommended)
**Cost:** $7/month  
**Memory:** 512MB → Upgrade to at least 1GB RAM

1. Go to your Render dashboard
2. Select your service
3. Click "Settings" → "Instance Type"
4. Upgrade to **Starter** plan (or higher)
5. Redeploy

This is the simplest solution if you want to keep using Render.

### Option 2: Railway (Free Tier - 1GB RAM)
**Cost:** Free tier includes $5 credit/month  
**Memory:** Up to 8GB on free tier

1. Sign up at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select `HebrewTranslator` repository
5. Add environment variable: `PORT=5005`
6. Deploy!

Railway's free tier is more generous than Render's.

### Option 3: Fly.io (Free Tier - 256MB shared)
**Cost:** Free tier available  
**Memory:** Upgrade to 1GB recommended

Similar deployment process to Railway.

### Option 4: Docker on DigitalOcean/AWS/GCP
**Cost:** ~$5-12/month depending on provider  
**Memory:** 1GB+ droplet/instance

Deploy using the included Dockerfile on any cloud provider.

### Option 5: Local Deployment (Free)
**Cost:** Free  
**Memory:** Uses your local machine

Run locally and expose via:
- **ngrok** (free tier available)
- **Cloudflare Tunnel** (free)
- **localtunnel** (free)

Example with ngrok:
```bash
# Start the app locally
python app.py

# In another terminal, expose it
ngrok http 5005
```

## Memory Optimizations Already Applied

This project includes:
- ✅ CPU-only PyTorch (smaller than GPU version)
- ✅ `low_cpu_mem_usage=True` during model loading
- ✅ `torch.no_grad()` during inference
- ✅ Garbage collection after each translation
- ✅ Model in eval mode

## Alternative: Lightweight Online API

If you need a truly free hosted solution, consider switching to an online API:

### Using `deep-translator` (requires internet):

**requirements.txt:**
```
Flask==3.0.0
deep-translator==1.11.4
Werkzeug==3.0.1
```

**app.py:**
```python
from deep_translator import GoogleTranslator
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    
    translator = GoogleTranslator(source='en', target='he')
    translation = translator.translate(text)
    
    return jsonify({"translation": translation})
```

This uses Google Translate API (free, no key needed) and uses < 100MB RAM, but requires internet for each translation.

## Recommendation

For your use case:
1. **Best for production:** Railway free tier or Render Starter ($7/month)
2. **Best for development:** Run locally with ngrok
3. **Best for true free hosting:** Switch to `deep-translator`

Choose based on your budget and whether you need offline translation capability.

