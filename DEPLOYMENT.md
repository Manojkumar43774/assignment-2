# Cloud Deployment Guide

## Deploy to Railway (Recommended)

Railway is the easiest way to deploy. It's free and integrates directly with GitHub.

### Step 1: Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Connect your GitHub account and select `Manojkumar43774/assignment-2`

### Step 2: Configure Environment Variables
Railway will automatically detect it's a Python FastAPI app.

Add these environment variables in Railway dashboard:

```
SECRET_KEY=production-secret-key-min-32-chars-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MODEL_TYPE=huggingface
MODEL_NAME=gpt2
HF_API_TOKEN=hf_xxxxx  # Get from https://huggingface.co/settings/tokens
DATABASE_URL=sqlite:///./app.db
DEBUG=False
```

### Step 3: Deploy
Click **"Deploy"** - Railway will automatically:
- Detect Python app
- Install dependencies
- Start the server

Your app will be live at a URL like: `https://assignment-2-production.up.railway.app`

---

## Alternative: Deploy to Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repo: `Manojkumar43774/assignment-2`
4. Set environment variables (same as above)
5. Deploy!

Your app will be at: `https://assignment-2.onrender.com`

---

## Alternative: Deploy to Heroku (Legacy)

```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Create app
heroku create assignment-2

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set MODEL_TYPE="huggingface"
heroku config:set HF_API_TOKEN="hf_xxxxx"

# Deploy
git push heroku main
```

---

## Using with Ollama on Cloud

If you want to use Ollama locally and connect from cloud:

1. Keep Ollama running locally on your machine
2. Expose it with ngrok:
```bash
brew install ngrok
ngrok http 11434
```

3. Set in cloud environment:
```
MODEL_TYPE=ollama
OLLAMA_BASE_URL=https://your-ngrok-url.ngrok.io
```

---

## Testing Your Deployed App

Once deployed, test with:

```bash
# Health check
curl https://your-app-url.com/health

# Register
curl -X POST https://your-app-url.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'

# Access API docs
https://your-app-url.com/docs
```

---

## Notes

- **Free tier** includes 512MB RAM (enough for FastAPI)
- **No credit card** needed for Railway/Render free tier
- **Logs** available in dashboard for troubleshooting
- **Auto-restart** on crash
- **SSL/HTTPS** included by default
