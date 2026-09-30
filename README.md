# Microservice with Open Models & Local Execution

A containerized FastAPI microservice running open models locally or via free-tier APIs, protected by JWT authentication and Pydantic v2 schema validation.

## Features

- **FastAPI** - Modern async web framework
- **JWT Authentication** - Secure API endpoints
- **Pydantic v2** - Data validation and serialization
- **Open Model Integration** - Using Ollama (local) or Hugging Face API (free-tier)
- **Docker** - Containerized deployment
- **Modular Architecture** - Clean separation of concerns

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- (Optional) Ollama for local model execution

### Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd assignment-2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Set environment variables
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

Server will be available at: `http://localhost:8000`

API Docs: `http://localhost:8000/docs`

### Running with Docker

```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Get JWT token

### AI Model
- `POST /model/generate` - Generate text using AI model
- `GET /model/status` - Check model status

## Documentation

- [Architecture](./docs/ARCHITECTURE.md) - System design and components
- [API Reference](./docs/API.md) - Detailed API documentation
- [Setup Guide](./docs/SETUP.md) - Deployment and configuration

## Project Structure

```
assignment-2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration and environment variables
│   ├── auth.py              # JWT authentication logic
│   ├── database.py          # Database setup (SQLite)
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   └── routers/
│       ├── auth.py          # Auth endpoints
│       └── model.py         # Model inference endpoints
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── docs/
    ├── ARCHITECTURE.md
    ├── API.md
    └── SETUP.md
```

## Environment Variables

See `.env.example` for required variables.

## License

MIT
