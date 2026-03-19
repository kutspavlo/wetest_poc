import sys
import os
import json
import time
import traceback

from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
import logging

# Import the utility class above
from jenkins_utils import UDTConfig

# Optional: Configure logging to output to console with DEBUG level
logging.basicConfig(level=logging.DEBUG)

# Optional: Specifically enable logging for urllib3 to see detailed HTTP request content
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("selenium").setLevel(logging.DEBUG)


def test_main():
    print("--- Python UDT Script Start ---")
    driver = None
    result_data = {}  # Used to return script execution results to the Jenkins plugin
    exec_result = True  # Used to return script execution results to the UDT platform
    try:
        # Load configuration
        udt_config = UDTConfig()
        # Obtain caps parameters from environment variables and set the name (job name on the UDT platform) -- it's
        # best to limit the name to 6 characters or less
        caps = udt_config.get_desired_capabilities(name="test")
        # Obtain the URL from environment variables
        remote_url = udt_config.get_remote_executor_url()

        # Initialize Driver
        options = AppiumOptions()
        options.load_capabilities(caps)
        driver = webdriver.Remote(command_executor=remote_url, options=options)

        # Settings required for the Jenkins plugin to fetch reports (otherwise, UDT report information cannot be
        # obtained in the Jenkins plugin)
        job_id = driver.capabilities.get('udt:jobId')
        test_id = driver.capabilities.get('udt:testId')
        result_data = {'testId': test_id, 'jobId': job_id, 'status': "running"}

        # Specific business logic (supports different types of tests)
        # Determine if it is a Web test (if the browserName field exists, it is Web)
        if caps.get("browserName"):
            print(">>> Detected WEB Test Mode")
            if caps.get("platformName") == "Android":
                print(">>> Detected Android WEB Test Mode")
                run_web_test_android(driver)  # Specific test script
            else:
                run_web_test_ios(driver)  # Specific test script
        else:
            print(">>> Detected NATIVE APP Test Mode")
            run_native_test(driver)  # Specific test script

        result_data['status'] = "success"
    except Exception as e:
        # Optional: Print full stack trace to console (for debugging in case of errors)
        print("\n" + "=" * 20 + " ERROR TRACEBACK " + "=" * 20)
        traceback.print_exc()
        print("=" * 57 + "\n")

        # Optional: Record brief error information in JSON report
        result_data['status'] = "failed"
        result_data['error'] = str(e) + "\n" + traceback.format_exc()  # Store stack trace in JSON as well
        exec_result = False
        sys.exit(1)

    finally:
        # Return results to Jenkins plugin
        result_path = os.environ.get('UDT_TEST_RESULT_PATH')
        if result_path:
            try:
                with open(result_path, 'w') as f:
                    json.dump(result_data, f)
            except Exception as e:
                print(f"Error writing result: {e}")

        if driver:
            # Return status to mark UDT job result
            driver.execute_script("udt:job-result={}".format("passed" if exec_result else "failed"))
            driver.quit()


def run_web_test_ios(driver):
    """ Web-specific test logic """
    print("Navigating to test page...")
    driver.get("https://www.google.com")
    time.sleep(2)

    # Take screenshot to prove the browser is open
    take_screenshot('web_page_loaded', driver)

    title = driver.title
    print(f"Page Title: {title}")
    # You can add Web element search logic here, e.g., driver.find_element(...)


def run_web_test_android(driver):
    """ Web-specific test logic """
    print("Navigating to test page...")
    targetUrl = "chrome://version";

    driver.get(targetUrl);

    # Screenshot: page loaded
    take_screenshot(driver, "1_Chrome_Version_Page");

    # Get basic page information
    currentUrl = driver.current_url
    title = driver.title
    print("Current URL: " + currentUrl)

    # Try executing JS to get User Agent (verify JS execution capability)
    print("Executing JS to get UserAgent...")
    userAgent = driver.execute_script("return navigator.userAgent;")
    print(">>> User Agent: " + userAgent);

    take_screenshot(driver, "2_JS_Executed");

    # Simple page interaction simulation (scrolling)
    # The chrome://version page is usually long, so scrolling can be tested
    print("Executing page scroll test...");
    driver.execute_script("window.scrollBy(0, 500)");
    time.sleep(1);
    take_screenshot(driver, "3_Scrolled_Down");

    # Scroll again
    driver.execute_script("window.scrollBy(0, 500)");
    time.sleep(1);
    take_screenshot(driver, "4_Scrolled_More");

    # Verify core functionality
    # As long as UserAgent is successfully obtained, it indicates that WebDriver's control over the browser is completely normal
    if userAgent and userAgent.strip():
        print(">>> Test passed: Successfully obtained browser UserAgent, WebDriver link is normal <<<");
    else:
        print(">>> Test failed: Unable to obtain UserAgent <<<");


def run_native_test(driver):
    """ Native App-specific test logic """
    time.sleep(2)
    take_screenshot('app_launched', driver)
    # Add App element search logic here


def take_screenshot(name, driver):
    try:
        base_dir = os.getcwd()
        screenshot_dir = os.path.join(base_dir, "screenshots")
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        driver.save_screenshot(os.path.join(screenshot_dir, f"{name}.png"))
    except Exception:
        pass


if __name__ == "__main__":
    test_main()
