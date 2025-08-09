# src/wanderwise/config.py

import logging
import os
from functools import lru_cache
from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Configure logging
# This basic configuration sets up logging to the console.
# In a production environment, you would configure this to output structured logs (e.g., JSON)
# and send them to a log aggregation service.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Explicitly load the .env file from the project root
# src/wanderwise/config.py is 3 levels deep from project root
project_root = Path(__file__).resolve().parent.parent.parent
# Debug the actual project root path
log = logging.getLogger(__name__)
log.info(f"Project root path: {project_root.absolute()}")
env_path = project_root / ".env"
log.info(f"Looking for .env at: {env_path.absolute()}")
load_dotenv(dotenv_path=env_path)

# Debug the environment variables
log = logging.getLogger(__name__)
log.info(f"Loaded .env from: {env_path}")
log.info(f"OPENAI_API_KEY exists: {bool(os.environ.get('OPENAI_API_KEY'))}")
if os.environ.get('OPENAI_API_KEY'):
    log.info(f"OPENAI_API_KEY length: {len(os.environ.get('OPENAI_API_KEY'))}")


class Settings(BaseSettings):
    """
    Application settings class.

    This class defines the configuration parameters for the WanderWise application.
    It uses pydantic-settings to automatically load values from environment variables.
    This provides a robust, type-safe way to manage application configuration.
    """
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)

    # Application metadata
    APP_NAME: str = "WanderWise"
    DEBUG: bool = Field(default=False, description="Enable debug mode.")
    
    def __hash__(self):
        """Make Settings hashable by returning a hash of its JSON representation."""
        return hash((
            self.APP_NAME,
            self.DEBUG,
            # Add other fields that should contribute to the hash
        ))
        
    def __eq__(self, other):
        """
        Compare Settings instances based on their attributes.
        This is required when __hash__ is defined.
        """
        if not isinstance(other, Settings):
            return False
        return all(
            getattr(self, field) == getattr(other, field)
            for field in self.model_dump()
        )
    
    # Maps configuration
    MAPBOX_ACCESS_TOKEN: str = Field(
        default="",
        description="Mapbox access token for interactive maps. Get one at https://account.mapbox.com/access-tokens/"
    )

    # OpenAI API configuration
    # The API key is loaded from the OPENAI_API_KEY environment variable.
    # It is stored as a SecretStr to prevent accidental exposure in logs or exceptions.
    OPENAI_API_KEY: SecretStr = Field(..., description="Your secret API key for OpenAI.")

    # Model configuration for the Pydantic BaseSettings class.
    model_config = SettingsConfigDict(
        env_file=str(env_path),    # Use the absolute path to the .env file
        env_file_encoding="utf-8",
        case_sensitive=False,      # Environment variable names are case-insensitive
        extra="ignore",            # Ignore extra fields
    )


# The @lru_cache decorator caches the result of the get_settings function.
# This means the Settings object is created only once, the first time it's requested.
# Subsequent calls to get_settings will return the cached instance, improving performance
# and preventing the .env file from being read multiple times.
@lru_cache
def get_settings() -> Settings:
    """
    Returns the application settings instance.

    This function is the single point of entry for accessing application settings.
    Using a function like this allows for dependency injection and easier testing,
    as the settings can be overridden during tests.
    """
    log = logging.getLogger(__name__)
    log.info("Loading application settings...")
    try:
        settings = Settings()
        log.info("Settings loaded successfully.")
        return settings
    except Exception as e:
        log.critical(f"Failed to load settings: {e}")
        raise


# Instantiate settings for easy access in other modules if needed,
# though using the get_settings function as a dependency is preferred.
settings = get_settings()
