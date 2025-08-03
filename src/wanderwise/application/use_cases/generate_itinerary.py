# src/wanderwise/application/use_cases/generate_itinerary.py

import logging

from ...domain.models.itinerary import Itinerary, ItineraryRequest
from ...domain.ports.llm_port import LLMPort

# Get a logger instance for this module.
log = logging.getLogger(__name__)


class GenerateItineraryUseCase:
    """
    Use case for generating a travel itinerary.

    This class encapsulates the business logic for creating an itinerary. It orchestrates
    the interaction between the domain models and the external services (via ports).
    """

    def __init__(self, llm_port: LLMPort):
        """
        Initializes the use case with a dependency on an LLM port.

        By using dependency injection, we decouple this use case from any specific
        LLM implementation. This makes the code more modular, testable, and
        maintainable. We can easily swap the LLM provider without changing
        this core application logic.

        Args:
            llm_port: An object that conforms to the LLMPort interface.
        """
        if not isinstance(llm_port, LLMPort):
            raise TypeError("llm_port must be an instance of LLMPort")
        self.llm_port = llm_port
        log.info(f"GenerateItineraryUseCase initialized with {type(llm_port).__name__}")

    async def execute(self, request: ItineraryRequest) -> Itinerary | None:
        """
        Executes the itinerary generation process.

        This method orchestrates the steps required to generate an itinerary:
        1. Logs the incoming request.
        2. Calls the injected LLM port to perform the generation.
        3. Logs the outcome (success or failure).
        4. Returns the generated itinerary or None.

        Args:
            request: An ItineraryRequest object containing user preferences.

        Returns:
            An Itinerary object if successful, otherwise None.
        """
        log.info(
            f"Executing itinerary generation for destination: '{request.destination}' "
            f"for {request.duration_days} days."
        )
        try:
            itinerary = await self.llm_port.generate_itinerary(request)
            if itinerary:
                log.info(f"Successfully generated itinerary: '{itinerary.trip_title}'")
                return itinerary
            else:
                log.warning("Itinerary generation returned None.")
                return None
        except Exception as e:
            log.error(f"An unexpected error occurred during itinerary generation: {e}", exc_info=True)
            # In a real-world scenario, you might raise a custom application-specific exception here.
            return None

