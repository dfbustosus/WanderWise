# Troubleshooting Guide

## Common Issues

### 1. App fails to start / Dependency errors
- Ensure you are using Python 3.11+
- Activate your virtual environment (`source venv/bin/activate`)
- Run `pip install -r requirements.txt`

### 2. .env not loaded / OPENAI_API_KEY not found
- Ensure `.env` is present in the project root and follows the format in `.env.example`
- Do not quote values in `.env` (Pydantic expects unquoted values)

### 3. Docker build fails
- Make sure `requirements.txt` is present and up to date
- Check `.dockerignore` excludes unnecessary files
- Use `docker build --no-cache .` to force a clean build

### 4. Itinerary generation fails / OpenAI errors
- Ensure your OpenAI API key is valid and has quota
- Check logs for error details
- The free tier may have rate limits

### 5. Static files or templates not loading
- Ensure you are running from the project root
- Check that `src/wanderwise/presentation/static/` and `src/wanderwise/presentation/templates/` exist and are populated

## Getting Help
- Check the [README](../README.md) for setup and usage
- Review logs for error messages
- If you encounter a bug, open an issue with details and logs
