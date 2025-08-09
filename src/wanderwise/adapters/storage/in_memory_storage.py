# src/wanderwise/adapters/storage/in_memory_storage.py

import logging
from typing import Dict, Optional, List
from uuid import uuid4
from ...domain.models.itinerary import Itinerary
from ...domain.ports.storage_port import StoragePort

log = logging.getLogger(__name__)

class InMemoryStorage(StoragePort):
    """
    An in-memory implementation of the StoragePort for development and testing.
    
    This implementation stores itineraries in a dictionary in memory and is not
    persistent across application restarts. It's suitable for development and
    testing purposes only.
    """
    
    def __init__(self):
        self._storage: Dict[str, Itinerary] = {}
        
    async def get_itinerary(self, itinerary_id: str) -> Optional[Itinerary]:
        """
        Retrieve an itinerary by its ID from memory.
        
        Args:
            itinerary_id: The unique identifier of the itinerary to retrieve.
            
        Returns:
            The requested Itinerary if found, None otherwise.
        """
        return self._storage.get(itinerary_id)
        
    async def save_itinerary(self, itinerary: Itinerary) -> bool:
        """
        Save an itinerary to memory.
        
        If the itinerary doesn't have an ID, one will be generated.
        
        Args:
            itinerary: The Itinerary object to save.
            
        Returns:
            Always returns True for this in-memory implementation.
        """
        # If it's a new itinerary, generate an ID
        if not hasattr(itinerary, 'id') or not itinerary.id:
            itinerary.id = str(uuid4())
            
        self._storage[itinerary.id] = itinerary
        log.info(f"Saved itinerary {itinerary.id} to in-memory storage")
        return True
        
    async def delete_itinerary(self, itinerary_id: str) -> bool:
        """
        Delete an itinerary from memory.
        
        Args:
            itinerary_id: The ID of the itinerary to delete.
            
        Returns:
            True if the itinerary was found and deleted, False otherwise.
        """
        if itinerary_id in self._storage:
            del self._storage[itinerary_id]
            log.info(f"Deleted itinerary {itinerary_id} from in-memory storage")
            return True
        return False
