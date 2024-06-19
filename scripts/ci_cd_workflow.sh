#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Print current working directory
echo "Current working directory: $(pwd)"

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# List installed packages
pip list

# Install Spacy and download the model
python -m pip install spacy
python -m spacy download en_core_web_sm

# Lint with flake8
flake8 src tests

# Run tests with pytest
pytest
