from utils import clone_repository, list_files_in_repository

repo_url = "https://github.com/example/repo.git"
local_path = "./cloned_repo"

clone_repository(repo_url, local_path)
files = list_files_in_repository(local_path)
print("Files in the cloned repository:", files)
