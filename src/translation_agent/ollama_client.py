"""
Ollama client for translation agent.
Provides utilities for interacting with Ollama models.
"""
import os
import json
import requests
from typing import List, Dict, Any, Optional
from icecream import ic


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = None):
        """
        Initialize Ollama client.
        
        Args:
            base_url (str): Base URL for Ollama API. Defaults to http://localhost:11434
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
    def list_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from Ollama.
        
        Returns:
            List[Dict]: List of available models with their metadata
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("models", [])
            
        except requests.exceptions.RequestException as e:
            ic(f"Error fetching Ollama models: {e}")
            return []
    
    def get_model_names(self) -> List[str]:
        """
        Get list of model names.
        
        Returns:
            List[str]: List of model names
        """
        models = self.list_models()
        return [model.get("name", "") for model in models if model.get("name")]
    
    def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from Ollama registry.
        
        Args:
            model_name (str): Name of the model to pull
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            payload = {"name": model_name}
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=300  # 5 minutes timeout for model pulling
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            ic(f"Error pulling model {model_name}: {e}")
            return False
    
    def is_model_available(self, model_name: str) -> bool:
        """
        Check if a model is available locally.
        
        Args:
            model_name (str): Name of the model to check
            
        Returns:
            bool: True if model is available, False otherwise
        """
        available_models = self.get_model_names()
        return model_name in available_models
    
    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.3,
        format: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            model (str): Model name to use
            prompt (str): Input prompt
            system (str, optional): System message
            temperature (float): Temperature for sampling
            format (str, optional): Response format (e.g., "json")
            stream (bool): Whether to stream the response
            
        Returns:
            str: Generated text
        """
        if system:
            full_prompt = f"System: {system}\\n\\nUser: {prompt}\\n\\nAssistant:"
        else:
            full_prompt = prompt
            
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "top_p": 1.0
            }
        }
        
        if format:
            payload["format"] = format
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.RequestException as e:
            ic(f"Error generating text with Ollama: {e}")
            raise Exception(f"Failed to generate text: {e}")
        except json.JSONDecodeError as e:
            ic(f"Error parsing Ollama response: {e}")
            raise Exception(f"Invalid JSON response: {e}")


# Global client instance
ollama_client = OllamaClient()


def get_available_models() -> List[str]:
    """Get list of available Ollama models."""
    return ollama_client.get_model_names()


def ensure_model_available(model_name: str) -> bool:
    """Ensure a model is available, pull if necessary."""
    if ollama_client.is_model_available(model_name):
        return True
    
    ic(f"Model {model_name} not found locally, attempting to pull...")
    return ollama_client.pull_model(model_name)