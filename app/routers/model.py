from fastapi import APIRouter, Depends, HTTPException, status
import requests
from app.schemas import GenerateRequest, GenerateResponse, ModelStatus
from app.auth import verify_token
from app.config import settings

router = APIRouter(prefix="/model", tags=["model"])


def get_ollama_response(prompt: str, max_tokens: int, temperature: float) -> str:
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ollama server not available")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_huggingface_response(prompt: str, max_tokens: int, temperature: float) -> str:
    if not settings.HF_API_TOKEN:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="HF_API_TOKEN not configured")

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{settings.MODEL_NAME}",
            headers={"Authorization": f"Bearer {settings.HF_API_TOKEN}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_length": max_tokens,
                    "temperature": temperature
                }
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest, username: str = Depends(verify_token)):
    if settings.MODEL_TYPE == "ollama":
        generated_text = get_ollama_response(request.prompt, request.max_tokens, request.temperature)
    elif settings.MODEL_TYPE == "huggingface":
        generated_text = get_huggingface_response(request.prompt, request.max_tokens, request.temperature)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown model type")

    return GenerateResponse(
        generated_text=generated_text,
        model=settings.MODEL_NAME,
        tokens_generated=len(generated_text.split())
    )


@router.get("/status", response_model=ModelStatus)
def status(username: str = Depends(verify_token)):
    if settings.MODEL_TYPE == "ollama":
        try:
            response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
            available = response.status_code == 200
        except:
            available = False
    else:
        available = bool(settings.HF_API_TOKEN)

    return ModelStatus(
        model=settings.MODEL_NAME,
        status="online" if available else "offline",
        available=available
    )
