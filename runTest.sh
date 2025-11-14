#!/bin/bash

export TESTMO_URL="https://YOUR-INSTANCE.testmo.net"
export TESTMO_TOKEN="YOUR_SECRET_API_TOKEN_HERE"

# Initialize test exit code
TEST_EXIT_CODE=0

echo "--- 2. Setting up Python Environment ---"
echo "Using system Python 3..."

echo "--- 3. Installing Dependencies ---"

# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "Python dependencies installed."

echo "--- 4. Running Pytest (using python3 -m) ---"
echo "Running test filter: $CASE_FUNC"

# Run pytest, generate 'results.xml', and capture the exit code
python3 -m pytest tests/ -k "$CASE_FUNC" --capture=no --junitxml=results.xml || TEST_EXIT_CODE=$?

echo "Pytest finished with exit code: $TEST_EXIT_CODE"

# Uploading Results to Testmo (using curl) ---

# Check if the results file was actually created
if [ ! -f "results.xml" ]; then
    echo "ERROR: Test results file 'results.xml' not found."
    echo "Please check your pytest command."
    exit 1
fi

echo "Uploading 'results.xml' to Testmo using curl..."


curl -u "api:$TESTMO_TOKEN" \
     -X POST "$TESTMO_URL/api/v1/projects/7/automation/submit" \
     -F "name=WeTest Run: $CASE_FUNC" \
     -F "source=WeTest" \
     -F "results[]=@results.xml"

UPLOAD_STATUS=$?
if [ $UPLOAD_STATUS -ne 0 ]; then
    echo "WARNING: Failed to upload results to Testmo. curl exited with code $UPLOAD_STATUS."
fi


echo "Exiting with original test code: $TEST_EXIT_CODE"
exit $TEST_EXIT_CODE