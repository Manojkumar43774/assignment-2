"""
Available AI Models Configuration
"""

AVAILABLE_MODELS = {
    "ollama": {
        "mistral": {
            "name": "Mistral 7B",
            "description": "Fast and efficient 7B parameter model",
            "provider": "Ollama",
            "size": "4GB",
            "url": "https://ollama.ai/library/mistral"
        },
        "llama2": {
            "name": "Llama 2 7B",
            "description": "Meta's Llama 2 model",
            "provider": "Ollama",
            "size": "4GB",
            "url": "https://ollama.ai/library/llama2"
        },
        "neural-chat": {
            "name": "Neural Chat",
            "description": "Optimized for conversation",
            "provider": "Ollama",
            "size": "4GB",
            "url": "https://ollama.ai/library/neural-chat"
        },
        "dolphin": {
            "name": "Dolphin",
            "description": "Dolphin uncensored model",
            "provider": "Ollama",
            "size": "4GB",
            "url": "https://ollama.ai/library/dolphin"
        },
        "orca-mini": {
            "name": "Orca Mini",
            "description": "Smaller, faster model",
            "provider": "Ollama",
            "size": "2GB",
            "url": "https://ollama.ai/library/orca-mini"
        }
    },
    "huggingface": {
        "gpt2": {
            "name": "GPT-2",
            "description": "OpenAI's GPT-2 model",
            "provider": "Hugging Face",
            "size": "Free API",
            "url": "https://huggingface.co/gpt2"
        },
        "distilgpt2": {
            "name": "DistilGPT-2",
            "description": "Smaller, faster version of GPT-2",
            "provider": "Hugging Face",
            "size": "Free API",
            "url": "https://huggingface.co/distilgpt2"
        },
        "t5-small": {
            "name": "T5 Small",
            "description": "Google's T5 text-to-text model",
            "provider": "Hugging Face",
            "size": "Free API",
            "url": "https://huggingface.co/t5-small"
        },
        "pegasus-cnn": {
            "name": "PEGASUS CNN",
            "description": "Summarization model",
            "provider": "Hugging Face",
            "size": "Free API",
            "url": "https://huggingface.co/google/pegasus-cnn_dailymail"
        },
        "bloom-560m": {
            "name": "BLOOM 560M",
            "description": "BigScience BLOOM model",
            "provider": "Hugging Face",
            "size": "Free API",
            "url": "https://huggingface.co/bigscience/bloom-560m"
        }
    }
}

def get_all_models():
    """Get all available models grouped by provider"""
    return AVAILABLE_MODELS

def get_models_by_provider(provider):
    """Get models for a specific provider"""
    return AVAILABLE_MODELS.get(provider, {})

def get_model_info(provider, model_id):
    """Get info for a specific model"""
    return AVAILABLE_MODELS.get(provider, {}).get(model_id, None)

def list_all_models_flat():
    """Get all models as a flat list"""
    result = []
    for provider, models in AVAILABLE_MODELS.items():
        for model_id, info in models.items():
            result.append({
                "id": model_id,
                "name": info["name"],
                "provider": provider,
                "description": info["description"],
                "size": info["size"]
            })
    return result
