#!/bin/bash

# Update package lists
sudo apt update
sudo apt install git curl -y


# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
  echo "Python3 not found. Installing..."
  sudo apt install python3-full
fi

# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# Get the virtual environment name (optional, modify as needed)
venv_name=".venv"

# Check if virtual environment already exists
if [ -d "$venv_name" ]; then
  echo "Virtual environment '$venv_name' already exists. Activating..."
  source "$venv_name/bin/activate"
else
  echo "Creating virtual environment '$venv_name'..."
  uv venv "$venv_name"
  source "$venv_name/bin/activate"
fi

# Install packages from requirements.txt
if [ -f "requirements.txt" ]; then
  echo "Installing packages from requirements.txt..."
  uv pip install -r requirements.txt
else
  echo "requirements.txt not found. Skipping package installation."
fi

echo "Done!"

# Deactivate the virtual environment (optional, uncomment if needed)
# deactivate
