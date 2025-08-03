# Usage Guide

## Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-fork-url>
   cd WanderWise
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your OpenAI API key.
5. **Run the app:**
   ```bash
   cd src
   python -m wanderwise.main
   ```
6. **Access the app:**
   - Open [http://localhost:8000](http://localhost:8000) in your browser.

## Docker

1. **Build the image:**
   ```bash
   docker build -t wanderwise .
   ```
2. **Run the container:**
   ```bash
   docker run --env-file .env -p 8000:8000 wanderwise
   ```

## Example Workflow
- Enter your destination, trip duration, travel style, and budget.
- Click "Generate My Itinerary" to receive a personalized AI-powered travel plan.
