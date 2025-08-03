# src/wanderwise/domain/ports/llm_port.py

from abc import ABC, abstractmethod
from typing import Dict, Any

from ..models.itinerary import Itinerary, ItineraryRequest


class LLMPort(ABC):
    """
    An abstract port defining the interface for a Large Language Model (LLM) service.

    This class defines the contract that any LLM gateway (adapter) must adhere to.
    By depending on this abstraction rather than a concrete implementation, the
    application's core logic remains decoupled from specific LLM providers (e.g., OpenAI,
    Google Gemini, Anthropic Claude). This allows for easier testing and swapping of
    LLM providers in the future.
    """

    @abstractmethod
    async def generate_itinerary(
        self, request: ItineraryRequest
    ) -> Itinerary | None:
        """
        Generates a travel itinerary based on the user's request.

        This method takes an ItineraryRequest object and should return a fully
        populated Itinerary object. The implementation of this method will handle
        prompt engineering, making the API call to the specific LLM, and parsing
        the response into the Itinerary domain model.

        Args:
            request: An ItineraryRequest object containing the user's travel preferences.

        Returns:
            An Itinerary object if the generation is successful and the response can be
            parsed correctly. Returns None if the generation fails or the response is
            invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def get_structured_prompt(self, request: ItineraryRequest) -> str:
        """
        Constructs a detailed, structured prompt for the LLM.

        This method is responsible for "prompt engineering". It takes the user's
        request and formats it into a precise set of instructions for the LLM,
        including the desired JSON output structure. Separating this logic allows
        for easier iteration and testing of the prompt itself.

        Args:
            request: An ItineraryRequest object.

        Returns:
            A string containing the full prompt to be sent to the LLM.
        """
        raise NotImplementedError

    @abstractmethod
    def get_response_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the expected LLM response.

        This schema is used to instruct the LLM to return a response in a specific
        JSON format, matching our Itinerary domain model. Using a schema greatly
        increases the reliability of receiving structured data.

        Returns:
            A dictionary representing the JSON schema of the Itinerary model.
        """
        raise NotImplementedError
