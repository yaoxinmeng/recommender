from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = "debug"
    BEDROCK_LLM_ID: str
    BEDROCK_USE_GUARDRAIL: bool
    BEDROCK_GUARDRAIL_ID: Optional[str] = None
    BEDROCK_GUARDRAIL_VERSION: Optional[str] = None

settings = Settings()