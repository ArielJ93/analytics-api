# pip install python-decouple
#from decouple import config as decouple_config
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# DATABASE_URL = decouple_config("DATABASE_URL", default="")
# DB_TIMEZONE = decouple_config("DB_TIMEZONE", default="UTC")

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    DATABASE_REDIS: str = Field(default="")
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()