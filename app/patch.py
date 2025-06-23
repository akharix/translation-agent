import os
import time
import requests
import json
from functools import wraps
from threading import Lock
from typing import Optional, Union

import gradio as gr
import openai
import translation_agent.utils as utils


RPM = 60
MODEL = ""
TEMPERATURE = 0.3
# Hide js_mode in UI now, update in plan.
JS_MODE = False
ENDPOINT = ""
OLLAMA_BASE_URL = ""
OLLAMA_MODEL = ""


# Add your LLMs here
def model_load(
    endpoint: str,
    base_url: str,
    model: str,
    api_key: Optional[str] = None,
    temperature: float = TEMPERATURE,
    rpm: int = RPM,
    js_mode: bool = JS_MODE,
):
    global client, RPM, MODEL, TEMPERATURE, JS_MODE, ENDPOINT
    ENDPOINT = endpoint
    RPM = rpm
    MODEL = model
    TEMPERATURE = temperature
    JS_MODE = js_mode

    match endpoint:
        case "OpenAI":
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        case "Groq":
            client = openai.OpenAI(
                api_key=api_key if api_key else os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1",
            )
        case "TogetherAI":
            client = openai.OpenAI(
                api_key=api_key if api_key else os.getenv("TOGETHER_API_KEY"),
                base_url="https://api.together.xyz/v1",
            )
        case "CUSTOM":
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
        case "Ollama":
            # Use direct Ollama integration instead of OpenAI compatibility
            global OLLAMA_BASE_URL, OLLAMA_MODEL
            OLLAMA_BASE_URL = "http://localhost:11434"
            OLLAMA_MODEL = model
            client = None  # We'll use direct Ollama calls
        case _:
            client = openai.OpenAI(
                api_key=api_key if api_key else os.getenv("OPENAI_API_KEY")
            )


def rate_limit(get_max_per_minute):
    def decorator(func):
        lock = Lock()
        last_called = [0.0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                max_per_minute = get_max_per_minute()
                min_interval = 60.0 / max_per_minute
                elapsed = time.time() - last_called[0]
                left_to_wait = min_interval - elapsed

                if left_to_wait > 0:
                    time.sleep(left_to_wait)

                ret = func(*args, **kwargs)
                last_called[0] = time.time()
                return ret

        return wrapper

    return decorator


@rate_limit(lambda: RPM)
def get_completion(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    model: str = "gpt-4-turbo",
    temperature: float = 0.3,
    json_mode: bool = False,
) -> Union[str, dict]:
    """
        Generate a completion using the OpenAI API.

    Args:
        prompt (str): The user's prompt or query.
        system_message (str, optional): The system message to set the context for the assistant.
            Defaults to "You are a helpful assistant.".
        model (str, optional): The name of the OpenAI model to use for generating the completion.
            Defaults to "gpt-4-turbo".
        temperature (float, optional): The sampling temperature for controlling the randomness of the generated text.
            Defaults to 0.3.
        json_mode (bool, optional): Whether to return the response in JSON format.
            Defaults to False.

    Returns:
        Union[str, dict]: The generated completion.
            If json_mode is True, returns the complete API response as a dictionary.
            If json_mode is False, returns the generated text as a string.
    """

    model = MODEL
    temperature = TEMPERATURE
    json_mode = JS_MODE

    # Handle Ollama endpoint differently
    if ENDPOINT == "Ollama":
        return _ollama_completion(prompt, system_message, model, temperature, json_mode)
    
    if json_mode:
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                top_p=1,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise gr.Error(f"An unexpected error occurred: {e}") from e
    else:
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                top_p=1,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise gr.Error(f"An unexpected error occurred: {e}") from e


def _ollama_completion(prompt: str, system_message: str, model: str, temperature: float, json_mode: bool) -> str:
    """Handle Ollama API calls directly."""
    full_prompt = f"System: {system_message}\n\nUser: {prompt}\n\nAssistant:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": 1.0
        }
    }
    
    if json_mode:
        payload["format"] = "json"
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
        
    except requests.exceptions.RequestException as e:
        raise gr.Error(f"Ollama API error: {e}") from e
    except json.JSONDecodeError as e:
        raise gr.Error(f"Invalid Ollama response: {e}") from e


def get_ollama_models():
    """Get list of available Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=30)
        response.raise_for_status()
        
        result = response.json()
        models = result.get("models", [])
        return [model.get("name", "") for model in models if model.get("name")]
        
    except requests.exceptions.RequestException:
        # Return default models if can't connect
        return ["llama3.1:8b", "llama3:8b", "mistral:7b", "qwen2:7b"]


def ensure_ollama_model(model_name: str) -> bool:
    """Ensure a model is available, pull if necessary."""
    try:
        # Check if model exists
        available_models = get_ollama_models()
        if model_name in available_models:
            return True
        
        # Try to pull the model
        payload = {"name": model_name}
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/pull",
            json=payload,
            timeout=300  # 5 minutes timeout
        )
        response.raise_for_status()
        return True
        
    except requests.exceptions.RequestException:
        return False


utils.get_completion = get_completion

one_chunk_initial_translation = utils.one_chunk_initial_translation
one_chunk_reflect_on_translation = utils.one_chunk_reflect_on_translation
one_chunk_improve_translation = utils.one_chunk_improve_translation
one_chunk_translate_text = utils.one_chunk_translate_text
num_tokens_in_string = utils.num_tokens_in_string
multichunk_initial_translation = utils.multichunk_initial_translation
multichunk_reflect_on_translation = utils.multichunk_reflect_on_translation
multichunk_improve_translation = utils.multichunk_improve_translation
multichunk_translation = utils.multichunk_translation
calculate_chunk_size = utils.calculate_chunk_size
