#!/bin/bash

TEST_EXIT_CODE=0

echo "--- 1. Setting up Python Environment ---"
echo "Using system Python 3..."

echo "--- 2. Installing Dependencies (using python3 -m pip) ---"
python3 -m pip install -r requirements.txt
python3 -m pip install testmo-cli
echo "Dependencies installed."

echo "--- 3. Running Pytest (using python3 -m) ---"
echo "Running test filter: $CASE_FUNC"

python3 -m pytest tests/ -k "$CASE_FUNC" --capture=no --junitxml=results.xml || TEST_EXIT_CODE=$?

echo "Pytest finished with exit code: $TEST_EXIT_CODE"


if [ ! -f "results.xml" ]; then
    echo "ERROR: Test results file 'results.xml' not found."
    echo "Please check your pytest command."
    exit 1
fi

echo "Uploading 'results.xml' to Testmo..."

python3 -m testmo automation:submit \
    --project-id 7 \
    --name "WeTest Run: $CASE_FUNC" \
    --source "WeTest" \
    --results results.xml

UPLOAD_STATUS=$?
if [ $UPLOAD_STATUS -ne 0 ]; then
    echo "WARNING: Failed to upload results to Testmo. CLI exited with code $UPLOAD_STATUS."
fi


echo "Exiting with original test code: $TEST_EXIT_CODE"
exit $TEST_EXIT_CODE