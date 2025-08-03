# src/wanderwise/application/services/itinerary_service.py

import logging

from ...domain.models.itinerary import Itinerary, ItineraryRequest
from ...domain.ports.llm_port import LLMPort

log = logging.getLogger(__name__)


class ItineraryService:
    """
    Application service for managing itinerary-related operations.

    This service encapsulates the core logic for creating and managing itineraries,
    acting as an intermediary between the use cases (the entry points) and the
    domain ports (the external interfaces).
    """

    def __init__(self, llm_port: LLMPort):
        """
        Initializes the ItineraryService with its dependencies.

        Args:
            llm_port: A concrete implementation of the LLMPort for interacting
                      with a language model.
        """
        self.llm_port = llm_port
        log.info(f"ItineraryService initialized with {type(llm_port).__name__}")

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

