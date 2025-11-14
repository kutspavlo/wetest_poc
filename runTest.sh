#!/bin/bash
# We MUST remove 'set -e' to ensure the Testmo upload
# runs even if the tests fail.
# We will capture the exit code manually.

# Initialize test exit code
TEST_EXIT_CODE=0

echo "--- 1. Setting up Python Environment ---"
echo "Using system Python 3..."

echo "--- 2. Installing Dependencies (using pip3) ---"
pip3 install -r requirements.txt
pip3 install testmo-cli # <-- Install Testmo CLI
echo "Dependencies installed."

echo "--- 3. Running Pytest (using python3 -m) ---"
echo "Running test filter: $CASE_FUNC"

# Run pytest, generate 'results.xml', and capture the exit code
# We use '|| TEST_EXIT_CODE=$?' to store the exit code if pytest fails
python3 -m pytest tests/ -k "$CASE_FUNC" --capture=no --junitxml=results.xml || TEST_EXIT_CODE=$?

echo "Pytest finished with exit code: $TEST_EXIT_CODE"

# --- 4. Uploading Results to Testmo ---

# Check if the results file was actually created
if [ ! -f "results.xml" ]; then
    echo "ERROR: Test results file 'results.xml' not found."
    echo "Please check your pytest command."
    # If the report is missing, we can't upload, so exit with an error
    exit 1
fi

echo "Uploading 'results.xml' to Testmo..."

# This command uses Environment Variables (TESTMO_URL, TESTMO_TOKEN)
# We use $CASE_FUNC in the run name for better tracking
python3 -m testmo automation:submit \
    --project-id 7 \
    --name "WeTest Run: $CASE_FUNC" \
    --source "WeTest" \
    --results results.xml

UPLOAD_STATUS=$?
if [ $UPLOAD_STATUS -ne 0 ]; then
    echo "WARNING: Failed to upload results to Testmo. CLI exited with code $UPLOAD_STATUS."
    # We don't exit here, we still want to report the original test failure
fi

# --- 5. Concluding WeTest Run ---

# Exit with the *original* pytest exit code.
# This tells WeTest if the tests passed (0) or failed (non-zero).
echo "Exiting with original test code: $TEST_EXIT_CODE"
exit $TEST_EXIT_CODE