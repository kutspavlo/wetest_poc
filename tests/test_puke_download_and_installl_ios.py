# -*- coding: UTF-8 -*-
import os
import time
import pytest
from appium import webdriver


# 1. Setup and Teardown using Pytest Fixtures
@pytest.fixture(scope="function")
def driver():
    print('\nSetting up Safari driver for WeTest iOS...')

    # Fetch WeTest dynamic variables
    udid = os.getenv("IOS_SERIAL")
    wda_ip = os.getenv("WDA_SERVER_IP")
    wda_port = os.getenv("WDA_SERVER_PORT")

    # Construct the WDA URL exactly as WeTest requires
    wda_url = f"http://{wda_ip}:{wda_port}/" if wda_ip and wda_port else None

    # Define Capabilities for Safari on Appium 1.22.3
    desired_caps = {
        'platformName': 'iOS',
        'automationName': 'XCUITest',
        'browserName': 'Safari',
        'deviceName': 'iOS',
        'newCommandTimeout': 600,

        # Cloud Environment variables injected by WeTest
        'udid': udid,

        # Safari-specific capabilities
        'autoAcceptAlerts': True,
        'safariInitialUrl': 'about:blank',
        'safariIgnoreFraudWarning': True
    }

    # Inject the pre-built WDA URL to bypass Xcode on Linux runners
    if wda_url:
        desired_caps['webDriverAgentUrl'] = wda_url
        desired_caps['usePrebuiltWDA'] = True

    # Connect to Appium 1.x server
    driver_instance = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    # Yield the driver to the test function
    yield driver_instance

    # TEARDOWN: This code runs after the test completes (pass or fail)
    print('\nTearing down driver...')
    driver_instance.quit()


# 2. The Test Case
def test_safari_google_search(driver):
    """
    Notice that 'driver' is passed as an argument.
    Pytest automatically injects the driver from the fixture above.
    """
    print('Starting Safari navigation test...')

    # Navigate directly to the URL
    driver.get("https://www.google.com")

    # Hard wait to allow cloud device network to load the page
    time.sleep(4)

    # 3. Pytest Assertions use standard Python 'assert'
    assert "Google" in driver.title, f"Expected 'Google' in title, but got: {driver.title}"
    print('Successfully validated Safari navigation.')


# 4. WeTest XML Reporting Integration
if __name__ == '__main__':
    # Fetch the WeTest upload directory (fallback to current folder)
    upload_dir = os.getenv("UPLOADDIR", ".")
    report_path = os.path.join(upload_dir, "report.xml")

    print(f"Running pytest and saving XML report to: {report_path}")

    # Run pytest programmatically and output the JUnit XML report WeTest needs
    pytest.main([
        "-v",  # Verbose output
        "-s",  # Allow print statements to show in console
        f"--junitxml={report_path}",  # Generate the XML report WeTest requires
        __file__  # Run this specific file
    ])