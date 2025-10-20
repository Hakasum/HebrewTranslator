# Hebrew Translator API - Quick Reference

## Translate Text

**Endpoint:** `POST http://localhost:5005/translate`

**Request Body (JSON):**
```json
{
  "text": "Hello world",
  "source": "en",
  "target": "he"
}
```

**Response (JSON):**
```json
{
  "translation": "שלום עולם",
  "source": "en",
  "target": "he",
  "time_seconds": 3.456
}
```

## Supported Languages

- `en` - English
- `es` - Spanish  
- `de` - German
- `he` - Hebrew

## Examples

**English to Hebrew:**
```bash
curl -X POST http://localhost:5005/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","source":"en","target":"he"}'
```

**Spanish to Hebrew:**
```bash
curl -X POST http://localhost:5005/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola mundo","source":"es","target":"he"}'
```

## Other Endpoints

- `GET /health` - Check API status
- `GET /languages` - List supported languages

