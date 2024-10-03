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
class Config:
    LOCAL_PATH = "/path/to/local/repo"
    OUTPUT_DIR = "/path/to/output/dir"
    HUGGINGFACE_API_KEY = "your_huggingface_api_key"
    MISTRAL_API_KEY = "your_mistral_api_key"
    OLLAMA_API_KEY = "your_ollama_api_key"
    OPENAI_API_KEY = "your_openai_api_key"
