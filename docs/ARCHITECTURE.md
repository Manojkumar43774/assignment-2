# System Architecture

## Overview

The microservice is built with FastAPI and consists of three main layers:

```
┌─────────────────────────────────────┐
│        API Layer (FastAPI)          │
│  ├─ Auth Endpoints                  │
│  └─ Model Endpoints                 │
├─────────────────────────────────────┤
│     Business Logic Layer            │
│  ├─ Authentication (JWT)            │
│  ├─ Validation (Pydantic v2)        │
│  └─ Model Integration               │
├─────────────────────────────────────┤
│        Data Layer                   │
│  ├─ SQLAlchemy ORM                  │
│  └─ SQLite Database                 │
├─────────────────────────────────────┤
│      External Services              │
│  ├─ Ollama (Local Models)           │
│  └─ Hugging Face (Free API)         │
└─────────────────────────────────────┘
```

## Components

### 1. Authentication Module (`app/auth.py`)
- **Password Hashing**: Bcrypt via Passlib
- **Token Generation**: JWT tokens with expiration
- **Token Verification**: HTTPBearer security scheme

### 2. Database Module (`app/database.py`)
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (local) or PostgreSQL (production)
- **Session Management**: Dependency injection

### 3. API Routers
- **Auth Router** (`app/routers/auth.py`): Register and login endpoints
- **Model Router** (`app/routers/model.py`): AI model inference endpoints

### 4. Data Validation (`app/schemas.py`)
- Pydantic v2 models for request/response validation
- Input constraints and type checking

## Authentication Flow

```
1. User registers/login → Create credentials
2. Server validates → Hash password (Bcrypt)
3. Generate JWT token → Return to client
4. Client sends token → Authorization header
5. Server verifies token → Extract username
6. Allow/Deny request based on token validity
```

## Model Integration

### Ollama (Local)
- Runs models locally using Ollama
- Supports: Mistral, Llama2, Neural-Chat, etc.
- Benefits: Privacy, no API costs, offline capability

### Hugging Face (Free API)
- Uses free-tier Hugging Face API
- Requires: API token
- Benefits: No local resources needed

## Deployment

### Docker
- Containerized FastAPI application
- Ollama service included in docker-compose
- Volume management for model persistence

### Environment Configuration
- Uses `.env` file for configuration
- Supports both local and cloud deployment
- Configurable model backends

## Security Considerations

1. **JWT Tokens**: Secure token-based authentication
2. **Password Hashing**: Bcrypt with salt
3. **CORS**: Configurable cross-origin requests
4. **Input Validation**: Pydantic schema validation
5. **Secret Key**: Must be changed in production
