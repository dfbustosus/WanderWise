<div align="center">
  <img src="docs/assets/wanderwise-logo.png" alt="WanderWise Logo" height="120"/>
  <h1>WanderWise</h1>
  <p><b>AI-powered travel itinerary generator for the modern explorer.</b></p>
  <p>
    <a href="https://github.com/yourusername/WanderWise/actions"><img src="https://img.shields.io/github/actions/workflow/status/yourusername/WanderWise/ci.yml?branch=main&label=build" alt="Build Status"></a>
    <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python 3.11"></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-Modern%20Web%20Framework-teal" alt="FastAPI"></a>
    <a href="https://platform.openai.com/"><img src="https://img.shields.io/badge/OpenAI-GPT--4o-green" alt="OpenAI"></a>
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Ready-blue" alt="Docker"></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/yourusername/WanderWise" alt="License"></a>
  </p>
  <br/>
  <img src="docs/assets/demo.gif" alt="WanderWise Demo" style="border-radius:8px; box-shadow:0 2px 8px #0002;" height="340"/>
  <br/>
</div>

---

> **Plan your next adventure in seconds.**
> WanderWise uses OpenAI and modern Python web tech to create beautiful, personalized travel itineraries—no signup, no hassle, just wander.

---

## ✨ Features
- 🧠 **AI Itineraries**: Personalized, day-by-day plans for any destination.
- ⚡ **Instant Results**: Lightning-fast, interactive UI (HTMX, Tailwind, Jinja2).
- 🔒 **Secure & Private**: No data stored, API key stays local.
- 🧩 **Modular Codebase**: Clean Architecture, easy to extend or audit.
- 🐳 **Docker-Ready**: Deploy anywhere, from laptop to cloud.
- 📖 **Full Documentation**: [See the docs/ folder](docs/)

---

## 📋 Table of Contents
- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)
- [Contact & Community](#-contact--community)

---

## 🚀 Quick Start

### Local
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI API key
cd src
python -m wanderwise.main
```
Visit [http://localhost:8000](http://localhost:8000)

### Docker
```bash
docker build -t wanderwise .
docker run --env-file .env -p 8000:8000 wanderwise
```

---

## 🏗️ Architecture
- **Backend**: FastAPI (Python 3.11), Clean Architecture
- **Frontend**: Jinja2, HTMX, Tailwind CSS
- **AI**: OpenAI GPT-4o, via robust adapter pattern
- **Docs**: See [`docs/`](docs/) for full technical details

---

## 🛠 Usage
1. Enter your destination, trip duration, travel style, and budget.
2. Click **Generate My Itinerary**.
3. Receive a beautiful, AI-powered travel plan.

---

## 🤝 Contributing
- Fork the repo & submit pull requests
- Follow Clean Architecture and PEP8
- All contributions welcome!

---

## 📚 Documentation
- [Architecture](docs/architecture.md)
- [Usage Guide](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## 🛡️ License
MIT License © 2025 David Usta & Contributors

---

## 💬 Contact & Community
- **Issues**: [GitHub Issues](https://github.com/yourusername/WanderWise/issues)
- **Email**: davidusta@example.com
- **Contributors**: [See contributors](https://github.com/yourusername/WanderWise/graphs/contributors)
- **Star this repo** if you like it!

---

<div align="center">
  <em>WanderWise: For explorers, by explorers. Happy travels! 🌍✈️</em>
</div>

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20Web%20Framework-teal)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)](https://platform.openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

> **AI-powered travel itinerary generator.**
> Build your dream trip in seconds with the help of OpenAI, FastAPI, HTMX, and Tailwind CSS.

---

## Features
- **AI-Powered Itineraries**: Personalized, day-by-day travel plans for any destination.
- **Modern UI**: Fast, interactive, and beautiful—no custom JS, just HTMX and Tailwind.
- **Clean Architecture**: Professional, maintainable, and extensible codebase.
- **Production-Ready**: Containerized with Docker, robust logging, and secure config.
- **Open Source**: Easy to contribute, audit, and extend.

---

## Quick Start

### Local Development
```bash
git clone https://github.com/yourusername/WanderWise.git
cd WanderWise
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI API key
cd src
python -m wanderwise.main
```
Visit [http://localhost:8000](http://localhost:8000)

### Docker
```bash
docker build -t wanderwise .
docker run --env-file .env -p 8000:8000 wanderwise
```

---

## Architecture
- **Backend**: FastAPI (Python 3.11), Clean Architecture
- **Frontend**: Jinja2, HTMX, Tailwind CSS
- **AI**: OpenAI GPT-4o, via robust adapter pattern
- **Docs**: See [`docs/`](docs/) for full technical details

---

## Documentation
- [Architecture](docs/architecture.md)
- [Usage Guide](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## Contributing
- Open a pull request or issue
- Follow Clean Architecture and PEP8
- All contributions welcome!

---

## License
MIT License 2025 David Usta & Contributors

---

## About
WanderWise was built to combine the power of modern Python, AI, and web UX best practices. Whether you're a developer, traveler, or AI enthusiast—this project is for you!