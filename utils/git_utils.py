import os
from git import Repo

def clone_repository(repo_url, local_path):
    """
    Clone a Git repository from the given URL to the specified local path.
    
    :param repo_url: URL of the Git repository to clone.
    :param local_path: Local directory path to clone the repository into.
    """
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    Repo.clone_from(repo_url, local_path)

def list_files_in_repository(local_path):
    """
    List all files in the cloned repository.
    
    :param local_path: Local directory path where the repository is cloned.
    :return: List of file paths in the repository.
    """
    if not os.path.exists(local_path):
        raise ValueError(f"Directory {local_path} does not exist.")
    
    file_list = []
    for root, dirs, files in os.walk(local_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    
    return file_list
def read_file_contents(file_path):
    """
    Read the contents of a file.
    
    :param file_path: Path to the file to read.
    :return: Contents of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()
