#!/bin/bash

# Define the directory structure
directories=(
    ".github/workflows"
    "docs/snippets"
    "agents"
    "config"
    "data"
    "models"
    "tests"
    "utils"
)

# Define the files to be created
files=(
    ".github/workflows/deploy-docs.yml"
    ".gitignore"
    "agents/__init__.py"
    "agents/comment_agent.py"
    "agents/doc_agent.py"
    "agents/litellm_integration.py"
    "config/__init__.py"
    "data/__init__.py"
    "models/__init__.py"
    "utils/__init__.py"
    "utils/embeddings.py"
    "utils/fetch_code.py"
    "config.py"
    "main.py"
    "mkdocs.yml"
    "requirements.txt"
)

# Create directories
for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    echo "Created directory: $dir"
done

# Create files
for file in "${files[@]}"; do
    touch "$file"
    echo "Created file: $file"
done

