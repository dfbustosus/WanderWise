# src/wanderwise/main.py

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException

from .config import get_settings
from .presentation.routers import itinerary_router
from .infrastructure.logging import configure_logging

# Configure logging for the application
configure_logging()
log = logging.getLogger(__name__)

# Create the FastAPI application
settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Travel Itinerary Planner",
    version="0.1.0",
    debug=settings.DEBUG,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files
static_dir = Path(__file__).parent / "presentation" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(itinerary_router.router)

# Setup templates
templates_dir = Path(__file__).parent / "presentation" / "templates"
templates = Jinja2Templates(directory=templates_dir)


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """Handle HTTP exceptions by rendering an error template."""
    log.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
    """Handle general exceptions by rendering an error template."""
    log.critical(f"Unhandled exception: {exc}", exc_info=True)
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": 500, "detail": "Internal Server Error"},
        status_code=500,
    )


# Root route - we don't need this since itinerary_router already handles /
# Removing to avoid redirect loop


if __name__ == "__main__":
    """Run the application using Uvicorn when executed directly."""
    import uvicorn
    log.info(f"Starting {settings.APP_NAME} in {'debug' if settings.DEBUG else 'production'} mode")
    uvicorn.run("wanderwise.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)

# Run the application using Uvicorn when executed directly
# cd src && python -m wanderwise.main