import os
import logging

class Config:
    # Load API keys from environment variables
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    if not HUGGINGFACE_API_KEY:
        logging.error("HUGGINGFACE_API_KEY is missing or invalid.")
        raise ValueError("Invalid API key")
    logging.info("HUGGINGFACE_API_KEY is valid.")

    @classmethod
    def validate_api_keys(cls):
        if not cls.HUGGINGFACE_API_KEY:
            logging.error("HUGGINGFACE_API_KEY is missing or invalid.")
            raise ValueError("Invalid API key")
        logging.info("API key validation successful.")
