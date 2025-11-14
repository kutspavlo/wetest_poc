#!/bin/bash

export TESTMO_TOKEN="testmo_api_eyJpdiI6Inl3S2tVdmw1U05mMGkvZy9pcFVLTHc9PSIsInZhbHVlIjoiT0lBV3lIWU8vdnhuN1JXbXMzVHJVV0ZoQk9XUlM1T3pFWXM0eEpjK1UzNEIxdVh5WVlJdWtxLzlvbGJQQ1FoMCIsIm1hYyI6ImY4ZTcyOTc5MGRlNDFkNjUyMTgxOGYyMjRiNWM2MWIzYjBmMzk1MzRiZmU0NjA5ZGQ0OWJjNmU1N2E2NWNlYzEiLCJ0YWciOiIifQ=="

TEST_EXIT_CODE=0

echo "--- Setting up Python Environment ---"
echo "Using system Python 3..."

echo "--- Installing Dependencies ---"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "Python dependencies installed."
echo "--- Installing jq... ---"
apt-get update && apt-get install -y jq

echo "--- Running Pytest ---"
echo "Running test filter: $CASE_FUNC"

python3 -m pytest tests/ -k "$CASE_FUNC" --capture=no --junitxml=results.xml || TEST_EXIT_CODE=$?

echo "Pytest finished with exit code: $TEST_EXIT_CODE"

# --- 5. Uploading Results to Testmo (Conditional) ---
REPORT_FLAG=$(echo "$EXTRA_INFO" | jq -r .REPORT_TO_TESTMO)

# Check if the UPLOAD_TO_TESTMO flag is set to "true"
if [ "$REPORT_FLAG" == "true" ]; then
    echo "REPORT_TO_TESTMO flag is 'true'. Proceeding with Testmo upload."

    # --- Start of Testmo-specific logic ---

    # Install Node.js (which includes npm) using nvm
    echo "Installing Node.js and npm via nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

    # Activate nvm in the current shell session
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    # Install a recent LTS version of Node (this installs node and npm)
    nvm install 18
    nvm use 18
    echo "Node/npm installation complete. node version: $(node -v), npm version: $(npm -v)"

    # Install Testmo CLI using the newly installed npm
    echo "Installing testmo-cli using npm..."
    npm install -g @testmo/testmo-cli
    echo "Testmo CLI installed."

    # Check if results file exists
    if [ ! -f "results.xml" ]; then
        echo "ERROR: Test results file 'results.xml' not found."
        # We don't exit here, just warn, so the script can finish
        echo "WARNING: Cannot upload to Testmo."
    else
        # Run the upload
        echo "Uploading 'results.xml' to Testmo..."
        testmo automation:run:submit \
            --instance https://a5test.testmo.net \
            --project-id 7 \
            --name "$CASE_FUNC-($(date +'%Y/%m/%d %H:%M'))" \
            --source "WeTest" \
            --results results.xml

        UPLOAD_STATUS=$?
        if [ $UPLOAD_STATUS -ne 0 ]; then
            echo "WARNING: Failed to upload results to Testmo. CLI exited with code $UPLOAD_STATUS."
        fi
    fi
    # --- End of Testmo-specific logic ---

else
    echo "REPORT_TO_TESTMO flag is not 'true' (Value: '$EXTRA_INFO.REPORT_TO_TESTMO'). Skipping Testmo reporting."
fi

# --- 6. Concluding WeTest Run ---

# Exit with the *original* pytest exit code.
echo "Exiting with original test code: $TEST_EXIT_CODE"
exit $TEST_EXIT_CODE