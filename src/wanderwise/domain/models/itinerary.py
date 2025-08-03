# src/wanderwise/domain/models/itinerary.py

from pydantic import BaseModel, Field
from typing import List, Optional

# This module defines the core data structures (entities) of the WanderWise application.
# These models are pure data containers and have no dependencies on any other part of the
# application, adhering to the principles of Clean Architecture. They represent the
# fundamental concepts of our domain.

class Activity(BaseModel):
    """
    Represents a single activity within a day of the itinerary.
    """
    time: str = Field(..., description="The suggested time for the activity (e.g., '09:00', 'Afternoon').")
    description: str = Field(..., description="A detailed description of the activity.")
    estimated_cost_usd: Optional[float] = Field(None, description="An optional estimated cost for the activity in USD.")
    booking_link: Optional[str] = Field(None, description="An optional link for booking the activity.")

class DailyPlan(BaseModel):
    """
    Represents the plan for a single day of the trip.
    """
    day: int = Field(..., gt=0, description="The day number of the trip (e.g., 1, 2, 3).")
    theme: str = Field(..., description="A theme for the day (e.g., 'Historical Exploration', 'Culinary Adventure').")
    activities: List[Activity] = Field(..., description="A list of activities planned for the day.")

class Itinerary(BaseModel):
    """
    Represents the complete travel itinerary for a destination.
    This is the main aggregate root of our domain model.
    """
    destination: str = Field(..., description="The city or region for the trip.")
    trip_title: str = Field(..., description="A catchy and descriptive title for the itinerary.")
    total_estimated_cost_usd: Optional[float] = Field(None, description="An optional overall estimated cost for the trip in USD.")
    daily_plans: List[DailyPlan] = Field(..., description="A list of daily plans that make up the itinerary.")

class ItineraryRequest(BaseModel):
    """
    Represents the user's request for generating an itinerary.
    This model is used to structure the input data from the user.
    """
    destination: str
    duration_days: int = Field(..., gt=0)
    travel_style: str
    budget: str # e.g., "Budget-friendly", "Mid-range", "Luxury"
