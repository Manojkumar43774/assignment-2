# NeuroAI - Complete Demo Flow

## 🎬 How to Demonstrate the Project

### Step 1: Open the Interactive Demo UI
Go to: **http://localhost:8000/static/index.html**

This interactive dashboard lets you:
- Register a new user
- Login to get JWT token
- Test all API endpoints
- See live JSON responses
- Demonstrate Pydantic v2 validation

---

## 📊 Complete Flow Explanation

### Flow Step 1: User Registration

**Endpoint:** `POST /auth/register`

**Request:**
```json
{
  "username": "demouser",
  "email": "demo@example.com",
  "password": "securepassword123"
}
```

**Response (Pydantic v2 Validated):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Explanation:**
- User creates account with email validation (Pydantic v2)
- Password is hashed with Bcrypt (never stored plain text)
- JWT token is generated immediately after registration
- Token expires based on `ACCESS_TOKEN_EXPIRE_MINUTES`

---

### Flow Step 2: User Login

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "username": "demouser",
  "password": "securepassword123"
}
```

**Response (Pydantic v2 Validated Token Schema):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Explanation:**
- Credentials are verified against hashed password in database
- JWT token contains username in "sub" claim
- Token includes expiration time (exp) and issued at (iat)
- Users save this token for subsequent authenticated requests

---

### Flow Step 3: Authorize with JWT Token

**How JWT Protection Works:**

Every protected endpoint requires:
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Behind the scenes:**
1. FastAPI extracts token from Authorization header
2. Token signature is verified using SECRET_KEY
3. Token expiration is checked
4. Username ("sub" claim) is extracted
5. Request is allowed if valid

---

### Flow Step 4: Generate Text (Protected Endpoint)

**Endpoint:** `POST /model/generate`

**Required Authorization:** Bearer Token (from login)

**Request:**
```json
{
  "prompt": "What is machine learning?",
  "max_tokens": 100,
  "temperature": 0.7
}
```

**Response (Pydantic v2 Validated):**
```json
{
  "generated_text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms and models that can...",
  "model": "mistral",
  "tokens_generated": 45
}
```

**Pydantic v2 Validation Applied:**
```python
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    max_tokens: int = Field(default=100, ge=1, le=2000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class GenerateResponse(BaseModel):
    generated_text: str
    model: str
    tokens_generated: int
```

**What's happening:**
- `prompt`: Validated to be 1-1000 characters
- `max_tokens`: Must be between 1-2000
- `temperature`: Must be between 0.0-2.0
- Response is validated against GenerateResponse schema
- All values are type-checked and coerced to correct types

---

### Flow Step 5: Check Model Status (Protected Endpoint)

**Endpoint:** `GET /model/status`

**Required Authorization:** Bearer Token

**Response (Pydantic v2 Validated):**
```json
{
  "model": "mistral",
  "status": "online",
  "available": true
}
```

**Explanation:**
- Checks if the configured AI model is accessible
- Returns status (online/offline)
- Shows model availability without making inference calls

---

## 🔒 JWT Authentication Security Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Registration                                        │
│    - Email validated (Pydantic)                            │
│    - Password hashed (Bcrypt)                              │
│    - Stored in SQLite database                             │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 2. JWT Token Generated                                      │
│    - Secret Key: Stored in .env                            │
│    - Algorithm: HS256                                       │
│    - Claims: username, exp, iat                            │
│    - Sent to client                                        │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 3. Client Stores Token                                      │
│    - Browser localStorage or session                       │
│    - Sent in Authorization header: "Bearer TOKEN"          │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 4. Server Verifies Token                                    │
│    - Extract from Authorization header                     │
│    - Verify signature with SECRET_KEY                      │
│    - Check expiration (exp claim)                          │
│    - Extract username from "sub" claim                     │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│ 5. Protected Endpoint Accessed                              │
│    - Request proceeds with username context                │
│    - Response validated with Pydantic v2                   │
│    - Return JSON response                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Live Demo Script

### 1. Show Health Check (No Auth Required)
```bash
curl http://localhost:8000/health
```
Response: `{"status": "healthy"}`

---

### 2. Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demoaccount",
    "email": "demo@example.com",
    "password": "Demo123456"
  }'
```
Response includes `access_token`

---

### 3. Show Token (Highlight JWT Structure)
```
Token format: Header.Payload.Signature

Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "demoaccount", "exp": 1234567890}
Signature: HMACSHA256(base64(header).base64(payload), SECRET_KEY)
```
Decode at https://jwt.io (shows token structure)

---

### 4. Generate Text WITH Authorization
```bash
TOKEN="your_token_from_register"

curl -X POST http://localhost:8000/model/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "max_tokens": 150,
    "temperature": 0.8
  }'
```

Response shows:
- `generated_text`: AI-generated response
- `model`: "mistral" (shows which model was used)
- `tokens_generated`: Actual tokens in response

---

### 5. Show What Happens WITHOUT Token
```bash
curl -X POST http://localhost:8000/model/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'
```
Response: `{"detail": "Invalid token"}` (401 Unauthorized)

---

## 🐳 Docker Deployment

### Build & Run with Docker
```bash
docker-compose up --build
```

Services:
- **FastAPI API**: Port 8000
- **Ollama**: Port 11434 (for local model execution)
- **SQLite**: Embedded in container

### Access from Container
- Demo UI: http://localhost:8000/static/index.html
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 🚀 Key Features to Highlight in Demo

1. **JWT Authentication**
   - Show registration creates token immediately
   - Show token is required for model endpoints
   - Show token expires and needs refresh

2. **Pydantic v2 Validation**
   - Try invalid email format (rejected)
   - Try password < 8 chars (rejected)
   - Try prompt > 1000 chars (rejected)
   - Try temperature > 2.0 (rejected)

3. **Protected Endpoints**
   - Show /health works without token
   - Show /model/generate fails without token
   - Show /model/status fails without token
   - Show proper error messages

4. **AI Model Integration**
   - Show /model/generate with different prompts
   - Show response format with generated_text, model, tokens_generated
   - Show model status check

5. **Database Persistence**
   - Register multiple users
   - Each can login independently
   - Data persists across requests

---

## 📱 Interactive Demo UI Features

The demo UI at `/static/index.html` provides:

- ✅ One-click registration
- ✅ One-click login
- ✅ Automatic token storage in localStorage
- ✅ Bearer token displayed for reference
- ✅ All API endpoints with real-time testing
- ✅ Beautiful responses in JSON format
- ✅ Error handling with clear messages
- ✅ Complete flow diagram
- ✅ Raw request examples
