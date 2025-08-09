# src/wanderwise/presentation/dependencies.py

from functools import lru_cache
from typing import Optional

from fastapi import Depends

from ..config import get_settings, Settings
from ..adapters.gateways.openai_gateway import OpenAIGateway
from ..adapters.storage.in_memory_storage import InMemoryStorage
from ..application.use_cases.generate_itinerary import GenerateItineraryUseCase
from ..application.services.itinerary_service import ItineraryService
from ..domain.ports.llm_port import LLMPort
from ..domain.ports.storage_port import StoragePort

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


def get_storage_port() -> StoragePort:
    """
    Dependency provider for the StoragePort.
    
    Returns:
        An instance of a class that implements the StoragePort interface.
    """
    # For now, we'll use the in-memory storage
    # In a production environment, you would use a real database implementation
    return InMemoryStorage()


def get_itinerary_service(
    llm_port: LLMPort = Depends(get_llm_port),
    storage_port: StoragePort = Depends(get_storage_port)
) -> ItineraryService:
    """
    Dependency provider for the ItineraryService.
    
    Args:
        llm_port: The LLM port implementation.
        storage_port: The storage port implementation.
        
    Returns:
        An instance of ItineraryService.
    """
    return ItineraryService(llm_port=llm_port, storage_port=storage_port)


def get_generate_itinerary_use_case(
    llm_port: LLMPort = Depends(get_llm_port)
) -> GenerateItineraryUseCase:
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
