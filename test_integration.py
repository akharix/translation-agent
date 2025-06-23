#!/usr/bin/env python3
"""
Test script for the complete Ollama integration.
"""
import sys
import os

# Add paths to find the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

import requests
from app.patch import get_ollama_models, ensure_ollama_model, model_load


def test_ollama_connection():
    """Test if we can connect to Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        response.raise_for_status()
        print("✅ Successfully connected to Ollama")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        return False


def test_get_models():
    """Test getting available models."""
    try:
        models = get_ollama_models()
        if models:
            print(f"✅ Found {len(models)} available models: {models}")
            return models[0] if models else None
        else:
            print("⚠️  No models found, will try with default model")
            return "llama3.1:8b"
    except Exception as e:
        print(f"❌ Failed to get models: {e}")
        return None


def test_model_loading(model_name):
    """Test loading a model."""
    try:
        model_load(
            endpoint="Ollama",
            base_url="http://localhost:11434",
            model=model_name,
            api_key=None,
            temperature=0.3,
            rpm=60
        )
        print(f"✅ Successfully loaded model: {model_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to load model {model_name}: {e}")
        return False


def test_simple_completion():
    """Test a simple completion."""
    try:
        # Import after model is loaded
        from app.patch import get_completion
        
        result = get_completion(
            prompt="Translate 'Hello, world!' from English to Spanish",
            system_message="You are a helpful translation assistant.",
            model="llama3.1:8b",
            temperature=0.3,
            json_mode=False
        )
        
        if result and len(result.strip()) > 0:
            print(f"✅ Translation test successful: {result.strip()}")
            return True
        else:
            print("❌ Translation test failed: empty response")
            return False
            
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Ollama Integration\n" + "="*40)
    
    # Test 1: Connection
    if not test_ollama_connection():
        print("\n❌ Cannot proceed without Ollama connection")
        return False
    
    # Test 2: Get models
    model = test_get_models()
    if not model:
        print("\n❌ Cannot proceed without available models")
        return False
    
    # Test 3: Load model
    if not test_model_loading(model):
        print(f"\n❌ Cannot proceed without loading model {model}")
        return False
    
    # Test 4: Simple completion
    if not test_simple_completion():
        print("\n❌ Translation functionality is not working")
        return False
    
    print("\n🎉 All tests passed! Ollama integration is working correctly.")
    print("\nYou can now run the web app with: python app/app.py")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)