from utils import clone_repository, list_files_in_repository
from agents import OpenAIAgent, OllamaAgent, HuggingFaceAgent, MistralAgent

repo_url = "https://github.com/example/repo.git"
local_path = "./cloned_repo"

clone_repository(repo_url, local_path)
files = list_files_in_repository(local_path)
print("Files in the cloned repository:", files)

# Example usage
openai_agent = OpenAIAgent(api_key="your-openai-api-key")
ollama_agent = OllamaAgent(api_key="your-ollama-api-key")
huggingface_agent = HuggingFaceAgent(api_key="your-huggingface-api-key")
mistral_agent = MistralAgent(api_key="your-mistral-api-key")

code = "def add(a, b):\n    return a + b"

comment = openai_agent.generate_comment(code)
documentation = ollama_agent.generate_documentation(code)

print("Generated Comment:", comment)
print("Generated Documentation:", documentation)
