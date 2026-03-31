# -*- coding: UTF-8 -*-
import os
import time
import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions


@pytest.fixture(scope="function")
def driver():
    print('\n--- Fetching WeTest Environment ---')
    udid = os.getenv("IOS_SERIAL")
    wda_url = os.getenv("WDA_HOST")

    print(f"Target UDID: {udid}")
    print(f"Target WDA URL: {wda_url}")
    print('-----------------------------------')

    # Use XCUITestOptions instead of desired_caps dictionary
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'
    options.device_name = 'iOS'

    # Let Appium handle the Safari launch natively
    options.browser_name = 'Safari'

    # WeTest Cloud specific capabilities
    options.udid = udid
    if wda_url:
        options.set_capability('webDriverAgentUrl', wda_url)
        options.set_capability('usePrebuiltWDA', True)

    options.new_command_timeout = 600
    options.auto_accept_alerts = True
    options.set_capability('safariInitialUrl', 'about:blank')

    print("Initializing Appium driver...")
    driver_instance = webdriver.Remote(
        command_executor="http://localhost:4723/wd/hub",
        options=options
    )

    yield driver_instance

    print('\nTearing down driver...')
    driver_instance.quit()


def test_safari_google_search(driver):
    # Appium already handles launching Safari and setting the context to WEBVIEW
    # when 'browserName' is used.

    print("Navigating to Google...")
    driver.get("https://www.google.com")

    # Allow the cloud device time to load the page over the network
    time.sleep(5)

    print(f"Current Title: {driver.title}")

    assert "Google" in driver.title, f"Expected 'Google' in title, but got: {driver.title}"
    print('Successfully validated Safari navigation.')


if __name__ == '__main__':
    upload_dir = os.getenv("UPLOADDIR", ".")
    report_path = os.path.join(upload_dir, "report.xml")

    pytest.main([
        "-v",
        "-s",
        f"--junitxml={report_path}",
        __file__
    ])