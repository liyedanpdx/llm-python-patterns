import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Default parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_MAX_TOKENS = 1024

# API Provider Configurations
API_PROVIDERS = {
    "gemini": {
        "api_key": GEMINI_API_KEY,
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-2.5-flash",
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "max_tokens": DEFAULT_MAX_TOKENS
    },
    "gemini-pro": {
        "api_key": GEMINI_API_KEY,
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-2.5-pro",
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "max_tokens": DEFAULT_MAX_TOKENS
    },
    "openai": {
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "max_tokens": DEFAULT_MAX_TOKENS
    },
    "openai-gpt3": {
        "api_key": OPENAI_API_KEY,
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo",
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "max_tokens": DEFAULT_MAX_TOKENS
    },
    "anthropic": {
        "api_key": ANTHROPIC_API_KEY,
        "base_url": "https://api.anthropic.com/v1",
        "model": "claude-3-sonnet-20240229",
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "max_tokens": DEFAULT_MAX_TOKENS
    }
}

def get_provider_config(provider: str) -> Dict[str, Any]:
    """Get configuration for specified provider"""
    if provider not in API_PROVIDERS:
        available = ", ".join(API_PROVIDERS.keys())
        raise ValueError(f"Unsupported provider: {provider}. Available: {available}")
    
    config = API_PROVIDERS[provider].copy()
    
    # Check if API key is available
    if not config.get("api_key"):
        raise ValueError(f"API key not found for provider: {provider}")
    
    return config