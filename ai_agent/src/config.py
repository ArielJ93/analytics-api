from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

#getting env variable
class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(default="")
    AI_MODEL: str = Field(default="")
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()