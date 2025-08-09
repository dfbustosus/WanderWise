# src/wanderwise/presentation/routers/itinerary_router.py

import logging
from pathlib import Path

from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional

from ...application.use_cases.generate_itinerary import GenerateItineraryUseCase
from ...application.services.itinerary_service import ItineraryService
from ...domain.models.itinerary import ItineraryRequest
from ...config import get_settings
from ..dependencies import (
    get_generate_itinerary_use_case, 
    get_llm_port,
    get_itinerary_service
)

# --- Router Setup ---
log = logging.getLogger(__name__)
router = APIRouter()

# Setup for templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# --- HTML Serving Endpoints ---

@router.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request):
    """
    Serves the main index page of the application.
    This page contains the form for users to input their travel preferences.
    """
    log.info("Serving index page.")
    settings = get_settings()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "config": {
            "MAPBOX_ACCESS_TOKEN": settings.MAPBOX_ACCESS_TOKEN
        }
    })


@router.post("/generate-itinerary", response_class=HTMLResponse, response_model=None)
async def generate_itinerary(
    request: Request,
    destination: str = Form(...),
    duration_days: int = Form(...),
    travel_style: str = Form(...),
    budget: str = Form(...),
    use_case: GenerateItineraryUseCase = Depends(get_generate_itinerary_use_case),
    itinerary_service: ItineraryService = Depends(get_itinerary_service),
):
    """
    Handles the form submission to generate a new itinerary.

    This endpoint is called by HTMX from the frontend. It receives the form data,
    invokes the appropriate use case, and returns an HTML fragment containing
    either the generated itinerary or an error message.
    """
    log.info(f"Received itinerary request for destination: {destination}")
    try:
        itinerary_request = ItineraryRequest(
            destination=destination,
            duration_days=duration_days,
            travel_style=travel_style,
            budget=budget,
        )

        itinerary = await use_case.execute(itinerary_request)

        if not itinerary:
            log.error("Itinerary generation failed. Use case returned None.")
            return templates.TemplateResponse(
                "partials/error.html",
                {"request": request, "error": "Failed to generate itinerary. Please try again."},
                status_code=500,
            )
    except Exception as e:
        log.error(f"Error generating itinerary: {e}", exc_info=True)
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "An unexpected error occurred. Please try again."},
            status_code=500,
        )

        log.info("Successfully generated itinerary. Rendering partial template.")
        settings = get_settings()
        # Save the itinerary to our storage
        await itinerary_service.storage_port.save_itinerary(itinerary)
        
        # Add the itinerary ID to the context for client-side use
        return templates.TemplateResponse(
            "partials/itinerary_display.html",
            {
                "request": request,
                "itinerary": itinerary,
                "config": {
                    "MAPBOX_ACCESS_TOKEN": get_settings().MAPBOX_ACCESS_TOKEN,
                    "ITINERARY_ID": getattr(itinerary, 'id', 'current')
                }
            },
        )
    except Exception as e:
        log.critical(f"An unexpected server error occurred: {e}", exc_info=True)
        # In case of an unexpected error, return a generic error message
        # to avoid exposing internal details.
        return templates.TemplateResponse(
            "partials/error_display.html",
            {"request": request, "error_message": "An unexpected server error occurred. Please contact support."},
        )

