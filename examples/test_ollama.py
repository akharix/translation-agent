#!/usr/bin/env python3
"""
Test script for Ollama translation functionality.
"""
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import translation_agent as ta
from translation_agent.ollama_client import get_available_models
from translation_agent.config import get_recommended_models


def test_model_availability():
    """Test if Ollama models are available."""
    print("Testing Ollama connection...")
    
    try:
        available_models = get_available_models()
        print(f"Available models: {available_models}")
        
        recommended_models = get_recommended_models()
        print(f"Recommended models: {recommended_models}")
        
        # Check if any recommended models are available
        available_recommended = [m for m in recommended_models if m in available_models]
        if available_recommended:
            print(f"Available recommended models: {available_recommended}")
            return available_recommended[0]  # Return first available model
        else:
            print("No recommended models available. Using first available model.")
            if available_models:
                return available_models[0]
            else:
                print("No models available! Please check Ollama connection.")
                return None
                
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return None


def test_translation(model_name):
    """Test translation functionality."""
    print(f"\nTesting translation with model: {model_name}")
    
    # Test data
    source_lang = "English"
    target_lang = "Spanish"
    country = "Mexico"
    source_text = "Hello, how are you today? I hope you're having a wonderful day!"
    
    try:
        print(f"Source text: {source_text}")
        print("Translating...")
        
        # Override the default model
        os.environ["OLLAMA_MODEL"] = model_name
        
        translation = ta.translate(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=source_text,
            country=country
        )
        
        print(f"Translation: {translation}")
        return True
        
    except Exception as e:
        print(f"Translation failed: {e}")
        return False


def main():
    """Main test function."""
    print("=== Ollama Translation Agent Test ===\n")
    
    # Test model availability
    model = test_model_availability()
    if not model:
        print("Cannot proceed with tests - no models available.")
        return False
    
    # Test translation
    success = test_translation(model)
    
    if success:
        print("\n✅ All tests passed! Ollama integration is working.")
    else:
        print("\n❌ Tests failed. Please check your configuration.")
    
    return success


if __name__ == "__main__":
    main()