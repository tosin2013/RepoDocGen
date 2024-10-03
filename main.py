def generate_documentation(repo_url, local_path, output_dir, agent_type):
    # Clone the repository
    clone_repository(repo_url, local_path)
    
    # List all files in the repository
    files = list_files_in_repository(local_path)
    
    # Initialize AI agent based on user input
    if agent_type == "huggingface":
        agent = HuggingFaceAgent(api_key="your_huggingface_api_key")
    elif agent_type == "mistral":
        agent = MistralAgent(api_key="your_mistral_api_key")
    elif agent_type == "ollama":
        agent = OllamaAgent(api_key="your_ollama_api_key")
    elif agent_type == "openai":
        agent = OpenAIAgent(api_key="your_openai_api_key")
    else:
        raise ValueError("Invalid agent type selected.")
    
    # Iterate over each file
    for file in files:
        file_path = os.path.join(local_path, file)
        code = read_file_contents(file_path)
        
        # Generate comments and documentation
        comments = agent.generate_comment(code)
        documentation = agent.generate_documentation(code)
        
        # Save the generated documentation in Markdown format
        output_file = os.path.join(output_dir, f"{file}.md")
        with open(output_file, 'w') as md_file:
            md_file.write(f"# {file}\n\n")
            md_file.write(f"## Comments\n{comments}\n\n")
            md_file.write(f"## Documentation\n{documentation}\n")

def build_mkdocs(output_dir):
    # Build MkDocs site
    subprocess.run(["mkdocs", "build", "--site-dir", output_dir])

if __name__ == "__main__":
    # User input
    repo_url = input("Enter the repository URL: ")
    local_path = input("Enter the local path to clone the repository: ")
    output_dir = input("Enter the output directory for documentation: ")
    agent_type = input("Select the AI agent (huggingface, mistral, ollama, openai): ")
    
    # Generate documentation
    generate_documentation(repo_url, local_path, output_dir, agent_type)
    
    # Build MkDocs site
    build_mkdocs(output_dir)
import os
import subprocess
from utils.git_utils import clone_repository, list_files_in_repository, read_file_contents
from agents.huggingface_agent import HuggingFaceAgent
from agents.mistral_agent import MistralAgent
from agents.ollama_agent import OllamaAgent
from agents.openai_agent import OpenAIAgent

def generate_documentation(repo_url, local_path, output_dir, agent_type):
    # Clone the repository
    clone_repository(repo_url, local_path)
    
    # List all files in the repository
    files = list_files_in_repository(local_path)
    
    # Initialize AI agent based on user input
    if agent_type == "huggingface":
        agent = HuggingFaceAgent(api_key="your_huggingface_api_key")
    elif agent_type == "mistral":
        agent = MistralAgent(api_key="your_mistral_api_key")
    elif agent_type == "ollama":
        agent = OllamaAgent(api_key="your_ollama_api_key")
    elif agent_type == "openai":
        agent = OpenAIAgent(api_key="your_openai_api_key")
    else:
        raise ValueError("Invalid agent type selected.")
    
    # Iterate over each file
    for file in files:
        file_path = os.path.join(local_path, file)
        code = read_file_contents(file_path)
        
        # Generate comments and documentation
        comments = agent.generate_comment(code)
        documentation = agent.generate_documentation(code)
        
        # Save the generated documentation in Markdown format
        output_file = os.path.join(output_dir, f"{file}.md")
        with open(output_file, 'w') as md_file:
            md_file.write(f"# {file}\n\n")
            md_file.write(f"## Comments\n{comments}\n\n")
            md_file.write(f"## Documentation\n{documentation}\n")
