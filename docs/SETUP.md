# Setup & Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip/poetry
- (Optional) Ollama for local model execution

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd assignment-2
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

**For Ollama (Local Model):**
```env
MODEL_TYPE=ollama
MODEL_NAME=mistral
OLLAMA_BASE_URL=http://localhost:11434
SECRET_KEY=your-super-secret-key
```

**For Hugging Face (Free API):**
```env
MODEL_TYPE=huggingface
MODEL_NAME=gpt2
HF_API_TOKEN=hf_xxxxxxxxxxxxx
SECRET_KEY=your-super-secret-key
```

### Step 5: Initialize Database
```bash
python -m app.database
```

### Step 6: Run Server
```bash
uvicorn app.main:app --reload
```

Access: http://localhost:8000/docs

---

## Docker Setup

### Prerequisites
- Docker & Docker Compose

### Using Ollama (Local Model)
```bash
docker-compose up --build
```

This will:
1. Build the FastAPI service
2. Start Ollama container
3. Expose API on port 8000
4. Expose Ollama on port 11434

**First run:**
The Ollama container needs to pull the model (~2-5GB). Once pulled, it's cached.

### Using Hugging Face API
Edit `docker-compose.yml`:

```yaml
environment:
  - MODEL_TYPE=huggingface
  - MODEL_NAME=gpt2
  - HF_API_TOKEN=hf_xxxxxxxxxxxxx
```

Then run:
```bash
docker-compose up --build
```

---

## Pull Models with Ollama

After starting the service, pull a model:

```bash
# From terminal
ollama pull mistral

# Or via API
curl http://localhost:11434/api/pull -d '{"name":"mistral"}'
```

Available models:
- `mistral` - 7B parameters (Recommended, balanced)
- `llama2` - 7B/13B/70B variants
- `neural-chat` - Optimized for chat
- `orca-mini` - Smaller, faster

---

## Production Deployment

### Environment Variables
```env
SECRET_KEY=production-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MODEL_TYPE=huggingface
MODEL_NAME=gpt2
HF_API_TOKEN=hf_xxxxx
DATABASE_URL=postgresql://user:pass@localhost/dbname
DEBUG=False
```

### Deployment Options

#### Option 1: Docker on Cloud (AWS/GCP/Azure)
```bash
docker build -t ai-microservice .
# Push to container registry
# Deploy to cloud platform
```

#### Option 2: Kubernetes
Create a deployment manifest:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-microservice
  template:
    metadata:
      labels:
        app: ai-microservice
    spec:
      containers:
      - name: api
        image: ai-microservice:latest
        ports:
        - containerPort: 8000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: secret-key
```

#### Option 3: Traditional Server
```bash
# Install
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Use Nginx as reverse proxy
# Use Systemd service for auto-restart
```

---

## Testing

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Test Model Inference
```bash
# Get token first (from login)
TOKEN="eyJhbGc..."

# Generate text
curl -X POST http://localhost:8000/model/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello world","max_tokens":100,"temperature":0.7}'

# Check status
curl -X GET http://localhost:8000/model/status \
  -H "Authorization: Bearer $TOKEN"
```

---

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `docker ps | grep ollama`
- Check Ollama URL matches `OLLAMA_BASE_URL`

### Model Not Found
- Pull model: `ollama pull mistral`
- Check model name in `.env`

### JWT Token Invalid
- Ensure `SECRET_KEY` is consistent
- Check token expiration: `ACCESS_TOKEN_EXPIRE_MINUTES`

### Database Locked
- Remove `app.db` and restart
- Check for multiple instances

---

## Performance Tuning

### For Ollama:
- Use smaller models for lower-end systems
- Increase Docker memory allocation: `-m 8g`
- Use GPU acceleration if available

### For Hugging Face:
- Use smaller models to reduce latency
- Implement request caching
- Use rate limiting

### General:
- Enable database indexing
- Use connection pooling
- Implement request pagination
