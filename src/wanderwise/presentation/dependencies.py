# src/wanderwise/presentation/dependencies.py

from functools import lru_cache

from ..config import get_settings, Settings
from ..adapters.gateways.openai_gateway import OpenAIGateway
from ..application.use_cases.generate_itinerary import GenerateItineraryUseCase
from ..domain.ports.llm_port import LLMPort

# This module is responsible for dependency injection. It decouples the web framework
# (FastAPI) from the application's core logic by providing functions that instantiate
# and return the necessary services and use cases.

@lru_cache(maxsize=1)
def get_llm_port(settings: Settings = get_settings()):
    """
    Dependency provider for the LLM port.

    This function instantiates and returns a concrete implementation of the LLMPort.
    The @lru_cache decorator ensures that the OpenAIGateway is only created once
    per application lifecycle, making it an efficient singleton.

    Args:
        settings: The application settings, injected automatically.

    Returns:
        An instance of a class that implements the LLMPort interface.
    """
    return OpenAIGateway(settings=settings)


def get_generate_itinerary_use_case(
    llm_port = get_llm_port()
):
    """
    Dependency provider for the GenerateItineraryUseCase.

    This function takes the LLMPort as a dependency and injects it into the
    use case. FastAPI will automatically resolve this dependency chain.

    Args:
        llm_port: The LLM port implementation, injected by FastAPI.

    Returns:
        An instance of the GenerateItineraryUseCase.
    """
    return GenerateItineraryUseCase(llm_port=llm_port)
