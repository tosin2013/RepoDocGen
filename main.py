if __name__ == "__main__":
    repo_url = "https://github.com/example/repo.git"
    local_path = "./cloned_repo"
    output_dir = "./docs"
    
    generate_documentation(repo_url, local_path, output_dir)
import os
from utils.git_utils import clone_repository, list_files_in_repository, read_file_contents
from agents.huggingface_agent import HuggingFaceAgent
from agents.mistral_agent import MistralAgent
from agents.ollama_agent import OllamaAgent
from agents.openai_agent import OpenAIAgent

def generate_documentation(repo_url, local_path, output_dir):
    # Clone the repository
    clone_repository(repo_url, local_path)
    
    # List all files in the repository
    files = list_files_in_repository(local_path)
    
    # Initialize AI agents
    huggingface_agent = HuggingFaceAgent(api_key="your_huggingface_api_key")
    mistral_agent = MistralAgent(api_key="your_mistral_api_key")
    ollama_agent = OllamaAgent(api_key="your_ollama_api_key")
    openai_agent = OpenAIAgent(api_key="your_openai_api_key")
    
    # Iterate over each file
    for file in files:
        file_path = os.path.join(local_path, file)
        code = read_file_contents(file_path)
        
        # Generate comments and documentation
        comments = huggingface_agent.generate_comment(code)
        documentation = mistral_agent.generate_documentation(code)
        
        # Save the generated documentation in Markdown format
        output_file = os.path.join(output_dir, f"{file}.md")
        with open(output_file, 'w') as md_file:
            md_file.write(f"# {file}\n\n")
            md_file.write(f"## Comments\n{comments}\n\n")
            md_file.write(f"## Documentation\n{documentation}\n")
