from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):

    model_config = ConfigDict(env_file=".env")
    
    openai_api_key: str
    openai_base_url: str

env = Settings()