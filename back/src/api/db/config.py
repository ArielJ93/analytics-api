# pip install python-decouple
#from decouple import config as decouple_config
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    REDIS_URI: str = Field(default="")

    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()