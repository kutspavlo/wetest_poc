import pytest
from appium import webdriver
import time


@pytest.mark.login
def test_user_launch_safari_ios():
    # 1. Define Desired Capabilities for Appium 1.22.3
    # Note: For Safari, we use 'browserName' instead of 'bundleId'
    desired_caps = {
        "platformName": "iOS",
        "automationName": "XCUITest",
        "browserName": "Safari",
        "deviceName": '<unknown>',
        "newCommandTimeout": 600
    }

    # 2. Connect to Appium Server
    # Appium 1.x strictly requires the '/wd/hub' path
    server_url = "http://127.0.0.1:4723/wd/hub"

    print("Connecting to Appium server and launching Safari...")
    driver = webdriver.Remote(server_url, desired_caps)

    try:
        # 3. Navigate to a URL
        # The .get() command works natively with browserName: 'Safari'
        driver.get("https://www.google.com")

        # Give the page a moment to load
        time.sleep(3)

        # Verify we are on the right page
        assert "Google" in driver.title
        print("Successfully launched Safari and navigated to Google.")

    finally:
        # 4. Clean up
        driver.quit()