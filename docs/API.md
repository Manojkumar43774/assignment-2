# API Reference

Base URL: `http://localhost:8000`

## Authentication Endpoints

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123",
  "email": "john@example.com"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

## Model Endpoints

### Generate Text
```http
POST /model/generate
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "prompt": "What is machine learning?",
  "max_tokens": 100,
  "temperature": 0.7
}
```

**Parameters:**
- `prompt` (string, required): Input text for generation
- `max_tokens` (integer, default: 100): Maximum tokens to generate
- `temperature` (float, default: 0.7): Sampling temperature (0.0-2.0)

**Response (200):**
```json
{
  "generated_text": "Machine learning is a subset of artificial intelligence...",
  "model": "mistral",
  "tokens_generated": 45
}
```

### Check Model Status
```http
GET /model/status
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "model": "mistral",
  "status": "online",
  "available": true
}
```

---

## Health Endpoints

### Health Check
```http
GET /health
```

**Response (200):**
```json
{
  "status": "healthy"
}
```

### Root Endpoint
```http
GET /
```

**Response (200):**
```json
{
  "message": "Welcome to AI Microservice",
  "docs_url": "/docs"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Ollama server not available"
}
```

---

## Authentication

All model endpoints require JWT authentication. Include the token in the header:

```
Authorization: Bearer {access_token}
```

---

## Interactive Documentation

Access Swagger UI for testing:
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
