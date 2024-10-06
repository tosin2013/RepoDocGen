import os

def clone_repository(repo_url, local_path):
    """Clone a Git repository to a local directory.

    :param repo_url: URL of the Git repository.
    :param local_path: Local directory to clone the repository to.
    """
    os.makedirs(local_path, exist_ok=True)
    os.system(f"git clone {repo_url} {local_path}")

def list_files_in_repository(local_path):
    """List all files in the cloned repository.

    :param local_path: Local directory where the repository is cloned.
    :return: List of file paths relative to the local_path.
    """
    files = []
    for root, _, filenames in os.walk(local_path):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), local_path)
            files.append(file_path)
    return files

def read_file_contents(file_path):
    """Read the contents of a file.

    :param file_path: Path to the file.
    :return: Contents of the file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
