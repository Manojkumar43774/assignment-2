from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000)
    max_tokens: int = Field(default=100, ge=1, le=2000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    model: str = Field(default="mistral", description="Model to use for generation")
    provider: str = Field(default="ollama", description="Model provider: ollama or huggingface")


class GenerateResponse(BaseModel):
    generated_text: str
    model: str
    provider: str
    tokens_generated: int


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    description: str
    size: str


class ModelsListResponse(BaseModel):
    models: list[ModelInfo]


class ModelStatus(BaseModel):
    model: str
    status: str
    available: bool
