# src/wanderwise/domain/ports/storage_port.py

from abc import ABC, abstractmethod
from typing import Optional, List
from ...domain.models.itinerary import Itinerary

class StoragePort(ABC):
    """
    Interface for storage operations related to itineraries.
    
    This port defines the contract that any storage adapter must implement
    to be used by the application layer for persisting and retrieving
    itinerary data.
    """
    
    @abstractmethod
    async def get_itinerary(self, itinerary_id: str) -> Optional[Itinerary]:
        """
        Retrieve an itinerary by its ID.
        
        Args:
            itinerary_id: The unique identifier of the itinerary to retrieve.
            
        Returns:
            The requested Itinerary if found, None otherwise.
        """
        pass
        
    @abstractmethod
    async def save_itinerary(self, itinerary: Itinerary) -> bool:
        """
        Save an itinerary to the storage.
        
        Args:
            itinerary: The Itinerary object to save.
            
        Returns:
            True if the save was successful, False otherwise.
        """
        pass
        
    @abstractmethod
    async def delete_itinerary(self, itinerary_id: str) -> bool:
        """
        Delete an itinerary from the storage.
        
        Args:
            itinerary_id: The ID of the itinerary to delete.
            
        Returns:
            True if the deletion was successful, False otherwise.
        """
        pass
