import os
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

# Create a global config instance
config = Config()
config = Config()
config = Config()
config = Config()
config = Config()
