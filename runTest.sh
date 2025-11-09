#!/bin/bash
# Exit immediately if any command fails
set -e

echo "--- 1. Setting up Python Environment ---"
echo "Using system Python 3..."

echo "--- 2. Installing Dependencies (using pip3) ---"
pip3 install -r requirements.txt

echo "--- 3. Running Pytest (using python3 -m) ---"
python3 -m pytest

echo "--- Test execution finished ---"
