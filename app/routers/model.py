from fastapi import APIRouter, Depends, HTTPException, status
import requests
from app.schemas import GenerateRequest, GenerateResponse, ModelStatus, ModelsListResponse
from app.auth import verify_token
from app.config import settings
from app.models_config import list_all_models_flat, get_model_info

router = APIRouter(prefix="/model", tags=["model"])


def get_ollama_response(prompt: str, max_tokens: int, temperature: float, model: str = "mistral") -> str:
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
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
        return f"[Demo Mode - Ollama Offline] Based on your prompt: '{prompt}'\n\nThis is a demo response. The actual response would come from the {model} model running in Ollama. The response is being generated with temperature={temperature} and max_tokens={max_tokens}."
    except Exception as e:
        return f"[Demo Mode] Error connecting to model: {str(e)}"


def get_huggingface_response(prompt: str, max_tokens: int, temperature: float, model: str = "gpt2") -> str:
    if not settings.HF_API_TOKEN:
        return f"[Demo Mode] Hugging Face API requires HF_API_TOKEN. Using {model} model.\n\nDemo response for prompt: '{prompt}'"

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
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
        return f"[Demo Mode] Error with {model}: {str(e)}"


@router.get("/list", response_model=ModelsListResponse)
def list_models(username: str = Depends(verify_token)):
    """List all available models"""
    models = list_all_models_flat()
    return ModelsListResponse(models=[{"id": m["id"], "name": m["name"], "provider": m["provider"], "description": m["description"], "size": m["size"]} for m in models])


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest, username: str = Depends(verify_token)):
    provider = request.provider
    model = request.model

    if provider == "ollama":
        generated_text = get_ollama_response(request.prompt, request.max_tokens, request.temperature, model)
    elif provider == "huggingface":
        generated_text = get_huggingface_response(request.prompt, request.max_tokens, request.temperature, model)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown provider")

    return GenerateResponse(
        generated_text=generated_text,
        model=model,
        provider=provider,
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
