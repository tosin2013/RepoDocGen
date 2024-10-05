import os
import subprocess
from urllib.parse import urlparse
from utils.git_utils import clone_repository, list_files_in_repository, read_file_contents
from agents.huggingface_agent import HuggingFaceAgent
from agents.mistral_agent import MistralAgent
from agents.ollama_agent import OllamaAgent
from agents.openai_agent import OpenAIAgent
from config import config  # Import the global config instance
import gradio as gr  # Ensure this import is correct

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

def generate_documentation(repo_url, local_path, output_dir, agent_type, uploaded_files):
    # Clone the repository or use uploaded files
    if repo_url:
        clone_repository(repo_url, local_path)
        files = list_files_in_repository(local_path)
    else:
        files = uploaded_files
    
    # Initialize AI agent based on user input
    if agent_type == "huggingface":
        agent = HuggingFaceAgent(api_key=config.HUGGINGFACE_API_KEY)
    elif agent_type == "mistral":
        agent = MistralAgent(api_key=config.MISTRAL_API_KEY)
    elif agent_type == "ollama":
        agent = OllamaAgent(api_key=config.OLLAMA_API_KEY)
    elif agent_type == "openai":
        agent = OpenAIAgent(api_key=config.OPENAI_API_KEY)
    else:
        raise ValueError("Invalid agent type selected.")
    
    # Iterate over each file
    documentation_content = ""
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
        output_file = os.path.join(output_dir, f"{os.path.basename(file)}.md")
        with open(output_file, 'w') as md_file:
            md_file.write(f"# {file}\n\n")
            md_file.write(f"## Comments\n{comments}\n\n")
            md_file.write(f"## Documentation\n{documentation}\n")
        
        # Append the generated documentation to the content
        with open(output_file, 'r') as md_file:
            documentation_content += md_file.read() + "\n\n"
    
    return documentation_content

def build_mkdocs(output_dir):
    # Build MkDocs site
    subprocess.run(["mkdocs", "build", "--site-dir", output_dir])

def gradio_interface(repo_url, agent_type, uploaded_files):
    local_path = config.LOCAL_PATH
    output_dir = config.OUTPUT_DIR
    
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
            gr.Textbox(label="Git Repository URL"),
            gr.Dropdown(choices=["huggingface", "mistral", "ollama", "openai"], label="Select AI Agent"),
            gr.File(file_count="multiple", label="Upload Code Files")
        ],
        outputs=gr.Markdown(label="Generated Documentation"),
        title="Documentation Generator",
        description="Generate documentation for your code using AI agents."
    )
    
    # Launch Gradio interface
    iface.launch()  # Correct method to launch the Gradio interface
