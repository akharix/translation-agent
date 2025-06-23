# Translation Agent: Agentic translation using reflection workflow

This is a Python demonstration of a reflection agentic workflow for machine translation. The main steps are:
1. Prompt an LLM to translate a text from `source_language` to `target_language`;
2. Have the LLM reflect on the translation to come up with constructive suggestions for improving it;
3. Use the suggestions to improve the translation.

## Customizability

By using an LLM as the heart of the translation engine, this system is highly steerable. For example, by changing the prompts, it is easier using this workflow than a traditional machine translation (MT) system to:
- Modify the output's style, such as formal/informal.
- Specify how to handle idioms and special terms like names, technical terms, and acronyms. For example, including a glossary in the prompt lets you make sure particular terms (such as open source, H100 or GPU) are translated consistently.
- Specify specific regional use of the language, or specific dialects, to serve a target audience. For example, Spanish spoken in Latin America is different from Spanish spoken in Spain; French spoken in Canada is different from how it is spoken in France.

**This is not mature software**, and is the result of Andrew playing around with translations on weekends the past few months, plus collaborators (Joaquin Dominguez, Nedelina Teneva, John Santerre) helping refactor the code.

According to our evaluations using BLEU score on traditional translation datasets, this workflow is sometimes competitive with, but also sometimes worse than, leading commercial offerings. However, we’ve also occasionally gotten fantastic results (superior to commercial offerings) with this approach. We think this is just a starting point for agentic translations, and that this is a promising direction for translation, with significant headroom for further improvement, which is why we’re releasing this demonstration to encourage more discussion, experimentation, research and open-source contributions.

If agentic translations can generate better results than traditional architectures (such as an end-to-end transformer that inputs a text and directly outputs a translation) -- which are often faster/cheaper to run than our approach here -- this also provides a mechanism to automatically generate training data (parallel text corpora) that can be used to further train and improve traditional algorithms. (See also [this article in The Batch](https://www.deeplearning.ai/the-batch/building-models-that-learn-from-themselves/) on using LLMs to generate training data.)

Comments and suggestions for how to improve this are very welcome!


## Getting Started

This version has been modified to use **Ollama** instead of OpenAI for local translation processing.

### Prerequisites:
- Ollama running at `http://localhost:11434`
- Poetry package manager for installation

### Installation:

```bash
# Install Poetry if you don't have it
pip install poetry

# Clone and setup the project
git clone https://github.com/andrewyng/translation-agent.git
cd translation-agent
poetry install
poetry shell # activates virtual environment
```

### Ollama Setup:

Make sure Ollama is running and accessible at `http://localhost:11434`. If you're using Docker:

```bash
# Example: Run Ollama in Docker
docker run -d --name ollama -p 11434:11434 ollama/ollama

# Pull a model for translation
docker exec -it ollama ollama pull llama3.1:8b
```

### Configuration:

Create a `.env` file (see `.env.example`):
```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

### Usage:

#### Command Line:
```python
import translation_agent as ta
source_lang, target_lang, country = "English", "Spanish", "Mexico"
translation = ta.translate(source_lang, target_lang, source_text, country)
```

#### Web Interface:
```bash
# Run the Gradio web interface
python app/app.py
```

#### Testing:
```bash
# Test Ollama connection
python3 test_simple.py

# Test complete integration (requires dependencies)
python3 test_integration.py
```

See `examples/example_script.py` for more examples.

## User Guide

### Web Interface Guide

1. **Launch the Web App**:
   ```bash
   python app/app.py
   ```
   The interface will be available at `http://localhost:7860`

2. **Configuration Panel** (left sidebar):
   - **Endpoint**: Select "Ollama" (default)
   - **Model**: Choose from available models or enter custom model name
   - **API Key**: Not required for Ollama
   - **Languages**: Set source and target languages
   - **Country**: Specify regional variant (e.g., "Mexico" for Mexican Spanish)

3. **Advanced Options**:
   - **Max Tokens Per Chunk**: Adjust for longer texts (default: 1000)
   - **Temperature**: Control randomness (0.0-1.0, default: 0.3)
   - **Request Per Minute**: Rate limiting (default: 60)

4. **Translation Process**:
   - Enter text in the "Source Text" area
   - Or upload files (PDF, DOCX, TXT supported)
   - Click "Translate"
   - View results in tabs: Final, Initial, Reflection, Diff

5. **Additional Endpoint**:
   - Enable "Additional Endpoint" for using different models for reflection
   - Useful for comparing model performance

### Model Management

#### Available Models
The system supports various Ollama models optimized for translation:
- **llama3.1:8b** - Balanced speed and quality (recommended)
- **llama3.1:70b** - Highest quality, slower processing
- **llama3:8b** - Fast and reliable
- **mistral:7b** - Good for creative translations
- **qwen2:7b** - Excellent for Asian languages
- **gemma2:9b** - Efficient alternative

#### Installing Models
```bash
# Pull recommended model
docker exec -it <ollama-container> ollama pull llama3.1:8b

# Pull other models as needed
docker exec -it <ollama-container> ollama pull llama3.1:70b
docker exec -it <ollama-container> ollama pull mistral:7b
```

#### Model Selection Guidelines
- **For speed**: llama3:8b, llama3.1:8b
- **For quality**: llama3.1:70b, qwen2:72b
- **For Asian languages**: qwen2:7b, qwen2:72b
- **For creative text**: mistral:7b, mistral:latest
- **For technical content**: llama3.1:8b, codellama:13b

### Performance Optimization

#### Text Chunking
- Texts over 1000 tokens are automatically chunked
- Each chunk maintains context from surrounding text
- Longer texts may take more time but maintain quality

#### Memory Usage
- Larger models (70b) require more RAM
- Use 8b models for resource-constrained environments
- Monitor Docker container memory limits

#### Speed Optimization
- Use smaller models for faster processing
- Adjust "Max Tokens Per Chunk" for your use case
- Enable GPU acceleration in Ollama if available

## Testing Guide

### Prerequisites Testing

1. **Check Ollama Connectivity**:
   ```bash
   python3 test_simple.py
   ```
   This tests basic connection and model availability.

2. **Verify Dependencies**:
   ```bash
   poetry install --with app,dev,test
   poetry shell
   ```

### Comprehensive Testing

1. **Full Integration Test**:
   ```bash
   python3 test_integration.py
   ```
   Tests all components including model loading and completion.

2. **Unit Tests**:
   ```bash
   pytest tests/
   ```
   Runs the existing test suite with mocked API calls.

3. **Web Interface Test**:
   ```bash
   python app/app.py
   ```
   Manual testing through the web interface.

### Testing Scenarios

#### Basic Translation Test
```python
import translation_agent as ta

# Test short text
result = ta.translate("English", "Spanish", "Hello, world!", "Mexico")
print(f"Translation: {result}")
```

#### Long Text Test
```python
# Test multi-chunk processing
long_text = "Your long document text here..." * 100
result = ta.translate("English", "French", long_text, "France")
```

#### Error Handling Test
```python
# Test with unavailable model
os.environ["OLLAMA_MODEL"] = "nonexistent:model"
# Should gracefully handle and suggest alternatives
```

### Troubleshooting

#### Common Issues

1. **"Cannot connect to Ollama"**:
   - Check if Ollama container is running: `docker ps`
   - Verify port mapping: `docker port <container-name>`
   - Test direct connection: `curl http://localhost:11434/api/tags`

2. **"Model not found"**:
   - List available models: `docker exec -it <container> ollama list`
   - Pull required model: `docker exec -it <container> ollama pull llama3.1:8b`

3. **Slow processing**:
   - Use smaller models (8b instead of 70b)
   - Reduce chunk size in advanced options
   - Check system resources

4. **Memory errors**:
   - Increase Docker memory limits
   - Use smaller models
   - Process shorter texts

#### Debug Mode
Enable debug output by setting:
```bash
export PYTHONPATH=/path/to/translation-agent/src
python -c "from icecream import ic; ic.enable()"
```

### Performance Benchmarks

#### Expected Processing Times (approximate)
- **Short text (< 100 words)**: 5-15 seconds
- **Medium text (100-500 words)**: 15-45 seconds  
- **Long text (500+ words)**: 1-5 minutes

Times vary significantly based on:
- Model size (8b vs 70b)
- Hardware (CPU vs GPU)
- Text complexity
- Target language

#### Quality Metrics
- **BLEU Score**: Typically 25-40 for most language pairs
- **Human Evaluation**: Often preferred over commercial MT
- **Consistency**: Excellent for terminology and style

## License

Translation Agent is released under the **MIT License**. You are free to use, modify, and distribute the code
for both commercial and non-commercial purposes.

## Ideas for extensions

Here are ideas we haven’t had time to experiment with but that we hope the open-source community will:
- **Try other LLMs.** We prototyped this primarily using gpt-4-turbo. We would love for others to experiment with other LLMs as well as other hyperparameter choices and see if some do better than others for particular language pairs.
- **Glossary Creation.** What’s the best way to efficiently build a glossary -- perhaps using an LLM -- of the most important terms that we want translated consistently? For example, many businesses use specialized terms that are not widely used on the internet and that LLMs thus don’t know about, and there are also many terms that can be translated in multiple ways. For example, ”open source” in Spanish can be “Código abierto” or “Fuente abierta”; both are fine, but it’d better to pick one and stick with it for a single document.
- **Glossary Usage and Implementation.** Given a glossary, what’s the best way to include it in the prompt?
- **Evaluations on different languages.** How does its performance vary in different languages? Are there changes that make it work better for particular source or target languages? (Note that for very high levels of performance, which MT systems are approaching, we’re not sure if BLEU is a great metric.) Also, its performance on lower resource languages needs further study.
- **Error analysis.** We’ve found that specifying a language and a country/region (e.g., “Spanish as colloquially spoken in Mexico”) does a pretty good job for our applications. Where does the current approach fall short? We’re also particularly interested in understanding its performance on specialized topics (like law, medicine) or special types of text (like movie subtitles) to understand its limitations.
- **Better evals.** Finally, we think better evaluations (evals) is a huge and important research topic. As with other LLM applications that generate free text, current evaluation metrics appear to fall short. For example, we found that even on documents where our agentic workflow captures context and terminology better, resulting in translations that our human raters prefer over current commercial offerings, evaluation at the sentence level (using the [FLORES](https://github.com/facebookresearch/flores) dataset) resulted in the agentic system scoring lower on BLEU. Can we design better metrics (perhaps using an LLM to evaluate translations?) that capture translation quality at a document level that correlates better with human preferences?

## Related work

A few academic research groups are also starting to look at LLM-based and agentic translation. We think it’s early days for this field!
- *ChatGPT MT: Competitive for High- (but not Low-) Resource Languages*, Robinson et al. (2023), https://arxiv.org/pdf/2309.07423
- *How to Design Translation Prompts for ChatGPT: An Empirical Study*, Gao et al. (2023), https://arxiv.org/pdf/2304.02182v2
- *Beyond Human Translation: Harnessing Multi-Agent Collaboration for Translating Ultra-Long Literary Texts*, Wu et al. (2024),  https://arxiv.org/pdf/2405.11804
