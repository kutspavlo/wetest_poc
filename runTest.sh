#!/bin/bash
# Exit immediately if any command fails
set -e

echo "--- 1. Setting up Python Environment ---"
echo "Using system Python 3..."

echo "--- 2. Installing Dependencies (using pip3) ---"
pip3 install -r requirements.txt

echo "--- 3. Running Pytest (using python3 -m) ---"
echo $CASE_FUNC
python3 -m pytest tests/ -k "$CASE_FUNC" --capture=no

echo "--- Test execution finished ---"
