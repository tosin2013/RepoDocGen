import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Load API keys from environment variables
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Default model choices
    DEFAULT_AGENT_TYPE = os.getenv("DEFAULT_AGENT_TYPE", "huggingface")

    # Local paths
    LOCAL_PATH = "./cloned_repo"
    OUTPUT_DIR = "./docs"

    @classmethod
    def validate_api_keys(cls):
        """Validate that the API key for the default agent type is not a default value."""
        default_keys = {
            "huggingface": "your_valid_huggingface_api_key",
            "mistral": "your_mistral_api_key",
            "ollama": "your_ollama_api_key",
            "openai": "your_openai_api_key"
        }
        default_value = default_keys.get(cls.DEFAULT_AGENT_TYPE)
        api_key_name = f"{cls.DEFAULT_AGENT_TYPE.upper()}_API_KEY"
        api_key_value = getattr(cls, api_key_name)

        if api_key_value == default_value:
            print(f"Error: {api_key_name} is set to the default value. Please update your .env file.")
            sys.exit(1)

# Create a global config instance
config = Config()

# Validate API keys
config.validate_api_keys()
