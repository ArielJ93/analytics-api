from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    AUTOMATION_API_KEY: str = Field(default="")
    COINGECKO_API_KEY: str = Field(default="")   
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()