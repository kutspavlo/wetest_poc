import sys
import os
import json
import traceback
import subprocess
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from jenkins_utils import UDTConfig


def run_ci_wrapper():
    print("--- Starting CI Wrapper ---")
    driver = None
    result_data = {}
    pytest_exit_code = 1  # Default to fail

    try:
        # 1. Load UDT Config
        udt_config = UDTConfig()
        caps = udt_config.get_desired_capabilities(name="CI_Test")
        remote_url = udt_config.get_remote_executor_url()

        # 2. Initialize a temporary driver to get IDs for the Jenkins Report
        # This acts as the "handshake" with the UDT platform
        options = AppiumOptions()
        options.load_capabilities(caps)
        driver = webdriver.Remote(command_executor=remote_url, options=options)

        # 3. Extract IDs required by Jenkins Plugin
        job_id = driver.capabilities.get('udt:jobId')
        test_id = driver.capabilities.get('udt:testId')
        result_data = {'testId': test_id, 'jobId': job_id, 'status': "running"}

        # 4. Export connection info for your EXISTING pytest structure
        # Your tests will read these env vars to know which device/URL to use
        os.environ['UDT_REMOTE_URL'] = remote_url
        os.environ['UDT_CAPS'] = json.dumps(caps)

        print(f">>> Triggering Pytest for Job: {job_id}")

        # 5. RUN YOUR EXISTING PYTEST STRUCTURE
        # This executes 'pytest' just like you do locally
        # You can add arguments like: ["pytest", "tests/my_test_folder", "--html=report.html"]
        process = subprocess.run(["pytest", "tests/test_puke_download_and_installl.py"], shell=False)
        pytest_exit_code = process.returncode

        result_data['status'] = "success" if pytest_exit_code == 0 else "failed"

    except Exception as e:
        print(f"Wrapper Error: {e}")
        traceback.print_exc()
        result_data['status'] = "failed"
        result_data['error'] = str(e)
        pytest_exit_code = 1

    finally:
        # 6. Report back to Jenkins Plugin
        result_path = os.environ.get('UDT_TEST_RESULT_PATH')
        if result_path:
            with open(result_path, 'w') as f:
                json.dump(result_data, f)

        # 7. Close the session and mark result on UDT platform
        if driver:
            status = "passed" if pytest_exit_code == 0 else "failed"
            driver.execute_script(f"udt:job-result={status}")
            driver.quit()

        sys.exit(pytest_exit_code)


if __name__ == "__main__":
    run_ci_wrapper()