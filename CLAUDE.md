# Claude Code Instructions for Translation Agent Project

## Project Overview
This translation agent uses an agentic workflow with reflection to perform high-quality machine translation using **local Ollama models**. The core process involves:
1. Initial translation using LLM
2. Reflection and critique of the translation
3. Improved translation based on reflection

**Key Update**: The project has been migrated from OpenAI to Ollama for local, privacy-focused translation processing.

## Development Guidelines

### Code Structure
- Main translation logic is in `src/translation_agent/utils.py`
- Ollama client integration in `src/translation_agent/ollama_client.py`
- Model configuration in `src/translation_agent/config.py`
- Web UI application is in `app/app.py` using Gradio
- App-specific Ollama handlers in `app/patch.py`
- Example usage in `examples/example_script.py`
- Tests are in `tests/test_agent.py`

### Key Functions to Understand
- `translate()`: Main entry point that handles chunking logic
- `one_chunk_translate_text()`: Core translation workflow for single chunks
- `multichunk_translation()`: Handles long texts by breaking into chunks
- `get_completion()`: Now supports both OpenAI and Ollama APIs
- `OllamaClient`: Direct Ollama API integration class
- `get_ollama_models()`: Retrieve available models from Ollama

### Development Preferences
- Use Poetry for dependency management
- Follow existing code patterns for prompt engineering
- Maintain the three-step translation process: initial → reflect → improve
- Use proper error handling for API calls
- Follow existing naming conventions and type hints

### Testing
- Run tests with: `poetry run pytest tests/`
- Mock external API calls in tests
- Test both single-chunk and multi-chunk translation paths
- Include edge cases like empty strings and special characters

### Code Quality
- Use ruff for linting: `poetry run ruff check`
- Use black for formatting: `poetry run black .`
- Use mypy for type checking: `poetry run mypy src tests`
- Maximum line length: 79 characters

### Environment Setup
- Ensure Ollama is running at `http://localhost:11434`
- Create `.env` file with Ollama configuration:
  ```
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_MODEL=llama3.1:8b
  ```
- Install dependencies: `poetry install`
- Activate virtual environment: `poetry shell`
- Pull recommended models: `ollama pull llama3.1:8b`

### Web UI Development
- UI is built with Gradio in `app/app.py`
- **Ollama is now the default endpoint** (was OpenAI)
- Supports multiple LLM endpoints (Ollama, OpenAI, Groq, TogetherAI)
- Dynamic model selection from available Ollama models
- Includes file upload for various formats (PDF, DOCX, TXT)
- Has diff visualization between initial and final translations
- API key field is optional for Ollama endpoint

### Performance Considerations
- Text is chunked when it exceeds MAX_TOKENS_PER_CHUNK (1000 tokens)
- Uses tiktoken for accurate token counting
- Implements rate limiting for API calls
- Supports parallel processing for multi-chunk translations

### Prompt Engineering Guidelines
- Use XML tags to structure prompts clearly
- Include specific instructions for accuracy, fluency, style, and terminology
- Support country-specific language variants
- Provide context for multi-chunk translations

### Extension Ideas
- Add support for more Ollama models and local LLM providers
- Implement glossary-based translation consistency
- Add translation quality metrics and BLEU scoring
- Support batch translation of multiple files
- Implement caching for repeated translations
- Add GPU acceleration support for Ollama
- Implement model auto-pulling when models aren't available
- Add translation memory for consistency across sessions

## Ollama Migration Details

### Migration Overview
The project was successfully migrated from OpenAI to Ollama for local translation processing. This involved:

1. **Core Library Changes**:
   - Modified `src/translation_agent/utils.py` to use Ollama API
   - Created `src/translation_agent/ollama_client.py` for direct integration
   - Added `src/translation_agent/config.py` for model management
   - Updated dependencies: replaced `openai` with `requests`

2. **Web App Integration**:
   - Updated `app/patch.py` to handle Ollama endpoint routing
   - Modified `app/app.py` to make Ollama the default
   - Added dynamic model selection from available Ollama models
   - Made API key optional for local Ollama usage

3. **Configuration Updates**:
   - Created `.env.example` with Ollama settings
   - Updated README with comprehensive Ollama setup instructions
   - Added testing scripts for validation

### Key Implementation Files

#### `src/translation_agent/ollama_client.py`
- `OllamaClient` class for API interaction
- Model listing and pulling functionality
- Error handling for connection issues
- Graceful fallbacks for offline scenarios

#### `src/translation_agent/config.py`
- Recommended model configurations
- Model-specific settings (temperature, max_tokens)
- Performance optimization guidelines

#### `app/patch.py`
- Ollama endpoint handling in `model_load()`
- Direct API calls via `_ollama_completion()`
- Model availability checking
- Rate limiting for local requests

### Migration Benefits
- **Privacy**: All processing happens locally
- **Cost**: No API fees for translation
- **Control**: Full control over model selection
- **Offline**: Works without internet connection
- **Customization**: Can fine-tune models for specific domains

### Migration Challenges Solved
- **API Compatibility**: Created abstraction layer for seamless switching
- **Model Management**: Automated model discovery and pulling
- **Error Handling**: Graceful degradation when models unavailable
- **Performance**: Optimized chunking for local processing
- **User Experience**: Maintained familiar web interface

## Common Tasks

### Adding a New Ollama Model
1. Add model name to `RECOMMENDED_MODELS` in `config.py`
2. Define model-specific configuration in `MODEL_CONFIGS`
3. Update documentation with model characteristics
4. Test translation quality with the new model

### Adding a New LLM Provider
1. Extend the `get_completion()` function to support the new provider
2. Update the web UI dropdown options
3. Add appropriate error handling and authentication
4. Update tests to cover the new provider
5. For local providers, follow the Ollama integration pattern

### Improving Translation Quality
1. Refine prompts in the reflection and improvement functions
2. Add domain-specific terminology handling
3. Implement better context preservation for multi-chunk texts
4. Add translation quality scoring

### Performance Optimization
1. Implement request batching for multiple chunks
2. Add async/await support for concurrent API calls
3. Implement intelligent chunking based on sentence boundaries
4. Add caching layer for repeated translations

## Architecture Notes
- The system uses a stateless approach - each translation is independent
- Chunking strategy preserves context by including surrounding text
- The reflection step is key to quality improvements
- Error handling focuses on graceful degradation
- **Ollama Integration**: Direct HTTP API calls to local Ollama instance at localhost:11434
- **Dual Architecture**: Core library supports both OpenAI and Ollama patterns
- **Model Management**: Dynamic model discovery and configuration
- **Fallback Strategy**: Graceful handling when models are unavailable

## Development Workflow

### Setting Up Ollama Development Environment
1. **Start Ollama container**:
   ```bash
   docker run -d --name ollama -p 11434:11434 ollama/ollama
   ```

2. **Pull development models**:
   ```bash
   docker exec -it ollama ollama pull llama3.1:8b
   docker exec -it ollama ollama pull mistral:7b
   ```

3. **Test connectivity**:
   ```bash
   curl http://localhost:11434/api/tags
   python3 test_simple.py
   ```

4. **Run development server**:
   ```bash
   poetry shell
   python app/app.py
   ```

### Debugging Ollama Issues
- **Connection errors**: Check Docker container status and port mapping
- **Model errors**: Verify model availability with `ollama list`
- **Performance issues**: Monitor container resources and model size
- **API errors**: Enable debug logging with `ic.enable()`

### Testing Strategy
1. **Unit tests**: Mock Ollama API calls for fast testing
2. **Integration tests**: Use real Ollama instance for full workflow
3. **Performance tests**: Benchmark different models and chunk sizes
4. **Quality tests**: Compare translations with commercial services

### Deployment Considerations
- **Resource Requirements**: 8GB+ RAM for 7B models, 32GB+ for 70B models
- **GPU Support**: Enable CUDA/ROCm for faster processing
- **Model Storage**: Plan for 4-40GB per model depending on size
- **Network**: Ollama runs locally, no external API dependencies
- **Security**: All processing happens on-premises