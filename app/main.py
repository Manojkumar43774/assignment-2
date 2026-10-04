from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.database import Base, engine
from app.routers import auth, model

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NeuroAI 🧠",
    description="Intelligent text generation powered by open models with JWT authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(model.router)

static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
def root():
    return {"message": "Welcome to NeuroAI 🧠", "app": "Intelligent Text Generation", "demo_url": "/static/index.html", "docs_url": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
