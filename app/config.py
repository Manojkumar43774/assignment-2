from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MODEL_TYPE: str = "ollama"  # ollama or huggingface
    MODEL_NAME: str = "mistral"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    HF_API_TOKEN: str = ""

    DATABASE_URL: str = "sqlite:///./app.db"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
