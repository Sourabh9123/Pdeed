from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Intelligence Platform"
    OPENAI_API_KEY: str = "placeholder_key_if_not_set"
    OPENAI_MODEL: str = "gpt-3.5-turbo-1106"

    class Config:
        env_file = ".env"

settings = Settings()
