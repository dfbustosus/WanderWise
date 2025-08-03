# Deployment Guide

## Production Deployment (Docker)

1. **Build the Docker image:**
   ```bash
   docker build -t wanderwise .
   ```
2. **Set up environment variables:**
   - Provide a `.env` file with your production OpenAI API key and `DEBUG=0`.
3. **Run the container:**
   ```bash
   docker run --env-file .env -p 8000:8000 wanderwise
   ```

## Cloud/Container Platforms
- Deploy the Docker image to any platform supporting containers (AWS ECS, Azure Container Apps, GCP Cloud Run, etc.).
- Mount or inject environment secrets securely.

## Security Best Practices
- Never commit real secrets or API keys to version control.
- Use unquoted values in `.env` for Pydantic compatibility.
- Restrict allowed hosts/origins in production (CORS settings).

## Health Checks
- The root endpoint (`/`) and `/docs` (FastAPI docs) can be used for basic health checks.

## Troubleshooting
- Check logs for errors (`docker logs <container-id>`).
- See [Troubleshooting](troubleshooting.md).
