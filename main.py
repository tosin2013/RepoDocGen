"""
Main module for the Documentation Generator application.
"""

import argparse
import logging
import os
import subprocess
import threading
from urllib.parse import urlparse

import gradio as gr  # Ensure this import is correct

from agents.huggingface_agent import HuggingFaceAgent
from agents.mistral_agent import MistralAgent
from agents.ollama_agent import OllamaAgent
from agents.openai_agent import OpenAIAgent
from utils.git_utils import clone_repository, list_files_in_repository, read_file_contents

from config import config  # Import the global config instance directly from config.py

# Configure logging
def setup_logging(log_level):
    """Configure logging for the application.

    :param log_level: Logging level to set.
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

def is_valid_repo_url(repo_url):
    """Check if the provided repository URL is valid.

    :param repo_url: URL of the Git repository.
    :return: True if valid, False otherwise.
    """
    try:
        result = urlparse(repo_url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_valid_code_file(file):
    """Check if the uploaded file is a valid code file.

    :param file: Uploaded file object.
    :return: True if valid, False otherwise.
    """
    valid_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.hpp', '.html', '.css', '.md']
    return file.name.endswith(tuple(valid_extensions))

def initialize_agent(agent_type):
    """Initialize the AI agent based on the user input.

    :param agent_type: Type of AI agent to initialize.
    :return: Initialized AI agent.
    """
    if agent_type == "huggingface":
        return HuggingFaceAgent(api_key=config.HUGGINGFACE_API_KEY)
    if agent_type == "mistral":
        return MistralAgent(api_key=config.MISTRAL_API_KEY)
    if agent_type == "ollama":
        return OllamaAgent(api_key=config.OLLAMA_API_KEY)
    if agent_type == "openai":
        return OpenAIAgent(api_key=config.OPENAI_API_KEY)
    raise ValueError("Invalid agent type selected.")

def generate_comments_and_documentation(agent, code):
    """Generate comments and documentation using the AI agent.

    :param agent: Initialized AI agent.
    :param code: Code to generate comments and documentation for.
    :return: Tuple containing generated comments and documentation.
    """
    comments = agent.generate_comment(code)
    documentation = agent.generate_documentation(code)
    return comments, documentation

def save_documentation(output_dir, file_name, comments, documentation):
    """Save the generated documentation in Markdown format.

    :param output_dir: Directory to save the documentation.
    :param file_name: Name of the file to save.
    :param comments: Generated comments.
    :param documentation: Generated documentation.
    """
    output_file = os.path.join(output_dir, f"{file_name}.md")
    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# {file_name}\n\n")
        md_file.write(f"## Comments\n{comments}\n\n")
        md_file.write(f"## Documentation\n{documentation}\n")

def generate_documentation(repo_url, paths, agent_type, uploaded_files, custom_output_dir=None):
    """Generate documentation for the provided repository or uploaded files.

    :param repo_url: URL of the Git repository.
    :param paths: Dictionary containing local_path and output_dir.
    :param agent_type: Type of AI agent to use.
    :param uploaded_files: List of uploaded files.
    :param custom_output_dir: Custom output directory (optional).
    :return: Generated documentation content.
    """
    output_dir = custom_output_dir if custom_output_dir else paths['output_dir']
    logging.info("Generating documentation for repo_url: %s, local_path: %s, output_dir: %s, agent_type: %s",
                 repo_url, paths['local_path'], output_dir, agent_type)
    
    if repo_url:
        clone_repository(repo_url, paths['local_path'])
        files = list_files_in_repository(paths['local_path'])
    else:
        files = uploaded_files
    
    agent = initialize_agent(agent_type)
    
    documentation_content = ""
    for file in files:
        if repo_url:
            file_path = os.path.join(paths['local_path'], file)
            code = read_file_contents(file_path)
        else:
            code = file.read().decode('utf-8')
        
        comments, documentation = generate_comments_and_documentation(agent, code)
        
        save_documentation(output_dir, os.path.basename(file), comments, documentation)
        
        with open(os.path.join(output_dir, f"{os.path.basename(file)}.md"), 'r', encoding='utf-8') as md_file:
            documentation_content += md_file.read() + "\n\n"
    
    return documentation_content

def build_mkdocs(output_dir):
    """Build the MkDocs site in the background.

    :param output_dir: Directory to build the MkDocs site.
    """
    logging.info("Building MkDocs site in directory: %s", output_dir)
    with subprocess.Popen(["mkdocs", "build", "--site-dir", output_dir, "--watch"], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        pass

def gradio_interface(repo_url, agent_type, uploaded_files, custom_output_dir=None):
    """Interface for generating documentation using Gradio.

    :param repo_url: URL of the Git repository.
    :param agent_type: Type of AI agent to use.
    :param uploaded_files: List of uploaded files.
    :param custom_output_dir: Custom output directory (optional).
    :return: Generated documentation content.
    """
    local_path = config.LOCAL_PATH
    output_dir = config.OUTPUT_DIR
    
    if repo_url and not is_valid_repo_url(repo_url):
        return "Invalid repository URL. Please provide a valid Git repository URL."
    
    if uploaded_files:
        for file in uploaded_files:
            if not is_valid_code_file(file):
                return f"Invalid file: {file.name}. Please upload valid code files."
    
    documentation_content = generate_documentation(repo_url, {'local_path': local_path, 'output_dir': output_dir}, agent_type, uploaded_files, custom_output_dir)
    
    build_mkdocs(output_dir)
    
    return documentation_content

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Documentation Generator")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level")
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Define Gradio interface
    iface = gr.Interface(
        fn=gradio_interface,
        inputs=[
            gr.Textbox(label="Git Repository URL"),
            gr.Dropdown(choices=["huggingface", "mistral", "ollama", "openai"], label="Select AI Agent"),
            gr.File(file_count="multiple", label="Upload Code Files"),
            gr.Textbox(label="Custom Output Directory (optional)")
        ],
        outputs=gr.Markdown(label="Generated Documentation"),
        title="Documentation Generator",
        description="Generate documentation for your code using AI agents."
    )
    
    # Run MkDocs in the background
    threading.Thread(target=build_mkdocs, args=(config.OUTPUT_DIR,)).start()
    
    # Launch Gradio interface
    iface.launch()
