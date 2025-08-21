import os
from dotenv import load_dotenv
from typing import Optional

def load_env():
    """Load environment variables from .env file"""
    load_dotenv()

def get_key(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(name, default)
