#!/usr/bin/env python3
"""
Simple test for Ollama connection.
"""
import requests
import json


def test_ollama():
    """Test basic Ollama functionality."""
    base_url = "http://localhost:11434"
    
    print("Testing Ollama connection...")
    
    # Test 1: Check if Ollama is running
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        response.raise_for_status()
        
        result = response.json()
        models = result.get("models", [])
        model_names = [model.get("name", "") for model in models if model.get("name")]
        
        print(f"✅ Connected to Ollama")
        print(f"✅ Found {len(model_names)} models: {model_names}")
        
        if not model_names:
            print("⚠️  No models available. You may need to pull a model first.")
            print("   Try: docker exec -it <ollama-container> ollama pull llama3.1:8b")
            return False
        
        # Test 2: Try a simple generation
        test_model = model_names[0]
        print(f"\\nTesting generation with model: {test_model}")
        
        payload = {
            "model": test_model,
            "prompt": "Translate 'Hello, world!' from English to Spanish. Respond only with the translation.",
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }
        
        response = requests.post(
            f"{base_url}/api/generate",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        if generated_text:
            print(f"✅ Generation successful: {generated_text}")
            print("\\n🎉 Ollama integration is working!")
            return True
        else:
            print("❌ Generation failed: empty response")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running at http://localhost:11434?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Ollama request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_ollama()
    if success:
        print("\\nThe translation app should work correctly with Ollama.")
    else:
        print("\\nPlease fix the issues above before using the translation app.")