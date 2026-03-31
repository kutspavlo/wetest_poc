import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions
import time


@pytest.mark.login
def test_user_launch_safari_ios():
    # WeTest usually maps the WDA port to 8100 locally on the Linux runner
    wda_url = "http://127.0.0.1:8100"

    # 1. Define Capabilities for a Linux Host (Bypassing Xcode)
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.browser_name = "Safari"
    options.device_name = "iPhone"
    options.new_command_timeout = 600

    # --- The Magic Flags for Linux / Cloud Execution ---
    # Tells Appium exactly where WDA is so it skips xcodebuild entirely
    options.set_capability("webDriverAgentUrl", wda_url)
    options.set_capability("usePrebuiltWDA", True)

    # Prevents Appium from trying to use macOS-specific tools for logs
    options.set_capability("skipLogCapture", True)

    # Handle Safari popups
    options.set_capability("autoAcceptAlerts", True)

    # 2. Connect to Appium Server
    server_url = "http://127.0.0.1:4723/wd/hub"

    print("Connecting to Appium server and launching Safari...")

    # Note: Using 'options' instead of 'desired_caps' fixes the DeprecationWarning in your logs
    driver = webdriver.Remote(command_executor=server_url, options=options)

    try:
        driver.get("https://www.google.com")
        time.sleep(3)
        assert "Google" in driver.title
        print("Successfully launched Safari!")

    finally:
        driver.quit()