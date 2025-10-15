# Groq LLM Setup Guide

## Quick Setup

1. **Get Groq API Key**:
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up/login and create an API key

2. **Set Environment Variable**:
   ```bash
   export GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Run the App**:
   ```bash
   ./runScript.sh
   ```

## Benefits of Groq

- ⚡ **Ultra-fast inference** - Responses in milliseconds
- 💰 **Cost-effective** - Much cheaper than OpenAI
- 🚀 **High throughput** - Can handle many concurrent requests
- 🔧 **Easy integration** - Compatible with OpenAI API format

## Models Available

- `llama3-8b-8192` (default) - Fast and efficient
- `mixtral-8x7b-32768` - More capable but slower
- `gemma-7b-it` - Google's efficient model

## Troubleshooting

- **No API Key**: App falls back to rule-based analysis
- **API Errors**: Check your internet connection and API key validity
- **Slow Responses**: Groq is usually very fast, check your connection

## Example Usage

```python
# The app automatically uses Groq when GROQ_API_KEY is set
# No code changes needed - just set the environment variable!
```
