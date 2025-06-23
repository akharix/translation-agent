"""
Configuration for Ollama models and settings.
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# Recommended models for translation tasks
RECOMMENDED_MODELS = [
    "llama3.1:8b",
    "llama3.1:70b", 
    "llama3:8b",
    "llama3:70b",
    "codellama:7b",
    "codellama:13b",
    "mistral:7b",
    "mistral:latest",
    "qwen2:7b",
    "qwen2:72b",
    "gemma2:9b",
    "gemma2:27b"
]

# Model configurations with specific settings
MODEL_CONFIGS = {
    "llama3.1:8b": {
        "max_tokens": 1000,
        "temperature": 0.3,
        "description": "Good balance of speed and quality for translation tasks"
    },
    "llama3.1:70b": {
        "max_tokens": 1200,
        "temperature": 0.2,
        "description": "High quality translations, slower processing"
    },
    "llama3:8b": {
        "max_tokens": 1000,
        "temperature": 0.3,
        "description": "Fast and reliable for most translation tasks"
    },
    "mistral:7b": {
        "max_tokens": 800,
        "temperature": 0.4,
        "description": "Good for creative translations"
    },
    "qwen2:7b": {
        "max_tokens": 1000,
        "temperature": 0.3,
        "description": "Excellent for Asian language translations"
    }
}

def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific model.
    
    Args:
        model_name (str): Name of the model
        
    Returns:
        Dict[str, Any]: Model configuration
    """
    return MODEL_CONFIGS.get(model_name, {
        "max_tokens": 1000,
        "temperature": 0.3,
        "description": "Default configuration"
    })

def get_recommended_models() -> List[str]:
    """
    Get list of recommended models for translation.
    
    Returns:
        List[str]: List of recommended model names
    """
    return RECOMMENDED_MODELS.copy()