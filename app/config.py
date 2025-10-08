from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()

