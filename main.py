import logging
from config.config import Config
from agents.huggingface_agent import HuggingFaceAgent

def setup_logging(log_level):
    logging.basicConfig(level=log_level)

def is_valid_repo_url(repo_url):
    # Existing code for validating repo URL
    pass

def is_valid_code_file(file):
    # Existing code for validating code file
    pass

def initialize_agent(agent_type):
    Config.validate_api_keys()
    api_key = Config.HUGGINGFACE_API_KEY
    if agent_type == "huggingface":
        return HuggingFaceAgent(api_key)
    # Existing code for initializing other agents
    pass

def generate_comments_and_documentation(agent, code):
    # Existing code for generating comments and documentation
    pass

def save_documentation(output_dir, file_name, comments, documentation):
    # Existing code for saving documentation
    pass

def generate_documentation(repo_url, paths, agent_type, uploaded_files, custom_output_dir=None):
    # Existing code for generating documentation
    pass

def build_mkdocs(output_dir):
    # Existing code for building mkdocs
    pass
