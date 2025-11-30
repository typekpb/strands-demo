#!/usr/bin/env bash

rm -rf lambda_package.zip

# Activate virtualenv and install deps
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create zip from site-packages
cd .venv/lib/python3*/site-packages
zip -r9 ../../../../lambda_package.zip .

# Add your code files
cd ../../../../
zip -g lambda_package.zip lambda_function.py agent.py
