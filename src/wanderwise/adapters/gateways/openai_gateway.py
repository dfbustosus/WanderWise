# src/wanderwise/adapters/gateways/openai_gateway.py

import json
import logging
from typing import Dict, Any

from openai import AsyncOpenAI, RateLimitError, APIError
from pydantic import ValidationError

from ...config import Settings
from ...domain.models.itinerary import Itinerary, ItineraryRequest
from ...domain.ports.llm_port import LLMPort

# Get a logger instance for this module.
log = logging.getLogger(__name__)


class OpenAIGateway(LLMPort):
    """
    A concrete implementation of the LLMPort for interacting with the OpenAI API.

    This class encapsulates all the logic required to communicate with OpenAI, including
    client initialization, prompt construction, API calls, and response parsing.
    """

    def __init__(self, settings: Settings):
        """
        Initializes the OpenAI gateway.

        Args:
            settings: The application settings object containing the API key.
        """
        # Store the API key instead of initializing the client
        self.api_key = settings.OPENAI_API_KEY.get_secret_value()
        self.model = "gpt-4o" # Using a powerful model capable of following JSON instructions
        log.info(f"OpenAIGateway initialized with model: {self.model}")
        
    def _get_client(self) -> AsyncOpenAI:
        """
        Creates a new client instance when needed.
        This prevents issues with deepcopy during FastAPI dependency injection.
        """
        return AsyncOpenAI(api_key=self.api_key)

    def get_response_schema(self) -> Dict[str, Any]:
        """Returns the JSON schema for the Itinerary model."""
        return Itinerary.model_json_schema()

    def get_structured_prompt(self, request: ItineraryRequest) -> str:
        """Constructs a detailed, structured prompt for the LLM."""
        prompt = f"""
        You are an expert travel agent named "WanderWise". Your task is to create a personalized travel itinerary.

        **User Request:**
        - Destination: {request.destination}
        - Duration: {request.duration_days} days
        - Travel Style: {request.travel_style}
        - Budget: {request.budget}

        **Instructions:**
        1. Create a detailed, day-by-day itinerary.
        2. For each day, provide a creative "theme".
        3. For each activity, provide a time, a description, and an optional estimated cost in USD.
        4. The entire response MUST be a single, valid JSON object that conforms to the provided schema.
        5. Do not include any introductory text, explanations, or markdown formatting outside of the JSON object.
        """
        return prompt

    async def generate_itinerary(self, request: ItineraryRequest) -> Itinerary | None:
        """
        Generates a travel itinerary by calling the OpenAI API.

        This method builds the prompt, makes the API call with JSON mode enabled,
        and parses the response into an Itinerary object.
        """
        prompt = self.get_structured_prompt(request)
        schema = self.get_response_schema()

        log.info(f"Sending request to OpenAI for destination: {request.destination}")
        try:
            # Get a fresh client instance for this request
            client = self._get_client()
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful travel planning assistant that only responds in JSON format."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object", "schema": schema},
                temperature=0.7,
                max_tokens=4096,
            )

            message_content = response.choices[0].message.content
            if not message_content:
                log.error("OpenAI response content is empty.")
                return None

            # Parse the JSON string from the response
            itinerary_data = json.loads(message_content)

            # Validate and create the Itinerary object using Pydantic
            itinerary = Itinerary.model_validate(itinerary_data)
            log.info(f"Successfully parsed and validated itinerary for '{itinerary.destination}'.")
            return itinerary

        except RateLimitError as e:
            log.error(f"OpenAI API rate limit exceeded: {e}")
            return None
        except APIError as e:
            log.error(f"OpenAI API error: {e}")
            return None
        except (ValidationError, json.JSONDecodeError) as e:
            log.error(f"Failed to validate or parse OpenAI response: {e}")
            return None
        except Exception as e:
            log.error(f"An unexpected error occurred while calling OpenAI: {e}", exc_info=True)
            return None
