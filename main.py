def generate_documentation(repo_url, local_path, output_dir, agent_type, uploaded_files):
    # Clone the repository or use uploaded files
    if repo_url:
        clone_repository(repo_url, local_path)
        files = list_files_in_repository(local_path)
    else:
        files = uploaded_files
    
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
        if repo_url:
            file_path = os.path.join(local_path, file)
            code = read_file_contents(file_path)
        else:
            code = file.read().decode('utf-8')
        
        # Generate comments and documentation
        comments = agent.generate_comment(code)
        documentation = agent.generate_documentation(code)
        
        # Save the generated documentation in Markdown format
        output_file = os.path.join(output_dir, f"{file.name}.md")
        with open(output_file, 'w') as md_file:
            md_file.write(f"# {file}\n\n")
            md_file.write(f"## Comments\n{comments}\n\n")
            md_file.write(f"## Documentation\n{documentation}\n")

def build_mkdocs(output_dir):
    # Build MkDocs site
    subprocess.run(["mkdocs", "build", "--site-dir", output_dir])

import gradio as gr

def gradio_interface(repo_url, agent_type, uploaded_files):
    local_path = "./cloned_repo"
    output_dir = "./docs"
    
    # Validate repository URL
    if repo_url and not is_valid_repo_url(repo_url):
        return "Invalid repository URL. Please provide a valid Git repository URL."
    
    # Validate uploaded files
    if uploaded_files:
        for file in uploaded_files:
            if not is_valid_code_file(file):
                return f"Invalid file: {file.name}. Please upload valid code files."
    
    # Generate documentation
    documentation_content = generate_documentation(repo_url, local_path, output_dir, agent_type, uploaded_files)
    
    # Build MkDocs site
    build_mkdocs(output_dir)
    
    return documentation_content

if __name__ == "__main__":
    # Define Gradio interface
    iface = gr.Interface(
        fn=gradio_interface,
        inputs=[
            gr.inputs.Textbox(label="Git Repository URL"),
            gr.inputs.Dropdown(choices=["huggingface", "mistral", "ollama", "openai"], label="Select AI Agent"),
            gr.inputs.File(file_count="multiple", label="Upload Code Files")
        ],
        outputs=gr.outputs.Markdown(label="Generated Documentation"),
        title="Documentation Generator",
        description="Generate documentation for your code using AI agents."
    )
    
    # Launch Gradio interface
    iface.launch()
import os
import subprocess
import gradio as gr
from urllib.parse import urlparse
from utils.git_utils import clone_repository, list_files_in_repository, read_file_contents
from agents.huggingface_agent import HuggingFaceAgent
from agents.mistral_agent import MistralAgent
from agents.ollama_agent import OllamaAgent
from agents.openai_agent import OpenAIAgent

def is_valid_repo_url(repo_url):
    """
    Check if the provided repository URL is valid.
    
    :param repo_url: URL of the Git repository.
    :return: True if valid, False otherwise.
    """
    try:
        result = urlparse(repo_url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_valid_code_file(file):
    """
    Check if the uploaded file is a valid code file.
    
    :param file: Uploaded file object.
    :return: True if valid, False otherwise.
    """
    valid_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.hpp', '.html', '.css', '.md']
    return file.name.endswith(tuple(valid_extensions))

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
