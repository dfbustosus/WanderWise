# WanderWise

AI-powered travel itinerary generator built with Python, FastAPI, and OpenAI.

## Overview

WanderWise is a modern web application that generates personalized travel itineraries using AI. Simply enter your destination, trip duration, and preferences to receive a comprehensive day-by-day travel plan.

## Features

- **AI-Generated Itineraries**: Personalized travel plans for any destination
- **Modern Tech Stack**: FastAPI, Jinja2, HTMX, and Tailwind CSS
- **Clean Architecture**: Modular, maintainable codebase
- **Docker Support**: Easy deployment and containerization

## Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/WanderWise.git
cd WanderWise

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run the application
cd src
python -m wanderwise.main
```

Visit http://localhost:8000 in your browser.

### Docker

```bash
# Build and run with Docker
docker build -t wanderwise .
docker run --env-file .env -p 8000:8000 wanderwise

# Or use docker-compose
docker-compose up
```

## Architecture

WanderWise follows Clean Architecture principles with clear separation of concerns:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and orchestration
- **Adapters**: External service integrations (OpenAI)
- **Infrastructure**: System concerns (logging, config)
- **Presentation**: FastAPI endpoints and templates

For more details, see [Architecture Documentation](docs/architecture.md).

## Documentation

- [Usage Guide](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

## Development

The project includes several development tools:

```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test
```

## License

MIT License 2025 David Usta & Contributors