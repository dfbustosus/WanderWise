# src/wanderwise/application/services/itinerary_service.py

import logging

from typing import Optional, List
from ...domain.models.itinerary import Itinerary, ItineraryRequest, DailyPlan
from ...domain.ports.llm_port import LLMPort
from ...domain.ports.storage_port import StoragePort

log = logging.getLogger(__name__)


class ItineraryService:
    """
    Application service for managing itinerary-related operations.

    This service encapsulates the core logic for creating and managing itineraries,
    acting as an intermediary between the use cases (the entry points) and the
    domain ports (the external interfaces).
    """

    def __init__(self, llm_port: LLMPort, storage_port: Optional[StoragePort] = None):
        """
        Initializes the ItineraryService with its dependencies.

        Args:
            llm_port: A concrete implementation of the LLMPort for interacting
                      with a language model.
            storage_port: Optional storage port for persisting itinerary data.
        """
        self.llm_port = llm_port
        self.storage_port = storage_port
        log.info(f"ItineraryService initialized with {type(llm_port).__name__} and {type(storage_port).__name__ if storage_port else 'no'} storage")

    async def create_itinerary(self, request: ItineraryRequest) -> Itinerary | None:
        """
        Creates a new itinerary by calling the configured LLM port.

        Args:
            request: An ItineraryRequest object containing the user's preferences.

        Returns:
            An Itinerary object if generation is successful, otherwise None.
        """
        log.info(f"Service creating itinerary for: {request.destination}")
        try:
            itinerary = await self.llm_port.generate_itinerary(request)
            if itinerary:
                log.info("Service successfully created itinerary.")
                # In a more complex app, this is where you might save the itinerary
                # to a database or trigger other events.
                return itinerary
            else:
                log.warning("LLM port returned no itinerary.")
                return None
        except Exception as e:
            log.error(f"Error in ItineraryService during creation: {e}", exc_info=True)
            return None

    async def reorder_activities(self, itinerary_id: str, day_number: int, new_order: List[str]) -> Optional[Itinerary]:
        """
        Reorder activities for a specific day in an itinerary.
        
        Args:
            itinerary_id: The ID of the itinerary to update
            day_number: The day number (1-based) to reorder activities for
            new_order: List of activity IDs in the new order
            
        Returns:
            Updated Itinerary if successful, None otherwise
        """
        if not self.storage_port:
            log.error("Cannot reorder activities: No storage port configured")
            return None
            
        try:
            # 1. Retrieve the current itinerary
            itinerary = await self.storage_port.get_itinerary(itinerary_id)
            if not itinerary:
                log.error(f"Itinerary not found: {itinerary_id}")
                return None
                
            # 2. Find the day to update
            day_to_update = next((day for day in itinerary.daily_plans if day.day == day_number), None)
            if not day_to_update:
                log.error(f"Day {day_number} not found in itinerary {itinerary_id}")
                return None
                
            # 3. Reorder activities
            try:
                day_to_update.reorder_activities(new_order)
            except ValueError as e:
                log.error(f"Invalid activity order: {e}")
                return None
                
            # 4. Save the updated itinerary
            updated = await self.storage_port.save_itinerary(itinerary)
            if updated:
                log.info(f"Successfully reordered activities for day {day_number} in itinerary {itinerary_id}")
                return itinerary
            else:
                log.error(f"Failed to save reordered activities for itinerary {itinerary_id}")
                return None
                
        except Exception as e:
            log.exception(f"Error reordering activities: {e}")
            return None
