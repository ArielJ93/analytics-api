from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

#getting env variable
class Settings(BaseSettings):
    STREAMLIT_API_KEY: str = Field(default="")
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()