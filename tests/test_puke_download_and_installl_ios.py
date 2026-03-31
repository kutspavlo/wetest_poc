# -*- coding: UTF-8 -*-
import os
import time
import pytest
from appium import webdriver


@pytest.fixture(scope="function")
def driver():
    print('\n--- Fetching WeTest Environment ---')
    udid = os.getenv("IOS_SERIAL")

    # NEW: WeTest now uses 'WDA_HOST' instead of separate IP/Port variables
    wda_url = os.getenv("WDA_HOST")

    print(f"Target UDID: {udid}")
    print(f"Target WDA URL: {wda_url}")
    print('-----------------------------------')

    desired_caps = {
        'platformName': 'iOS',
        'automationName': 'XCUITest',
        'deviceName': 'iOS',
        'newCommandTimeout': 600,

        # Launch Safari natively to bypass Xcode WebKit version checks
        'bundleId': 'com.apple.mobilesafari',

        'udid': udid,
        'webDriverAgentUrl': wda_url,
        'usePrebuiltWDA': True,

        'autoAcceptAlerts': True
    }

    print("Initializing Appium driver...")
    driver_instance = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    yield driver_instance

    print('\nTearing down driver...')
    driver_instance.quit()


def test_safari_google_search(driver):
    print('Starting Safari native launch...')

    # Wait for the app to fully open
    time.sleep(4)

    print(f'Available Contexts: {driver.contexts}')

    # We must switch to the WEBVIEW context to interact with the web elements
    webview_context = None
    for context in driver.contexts:
        if 'WEBVIEW' in context:
            webview_context = context
            break

    if webview_context:
        print(f"Switching to context: {webview_context}")
        driver.switch_to.context(webview_context)
    else:
        print("WARNING: Could not find WEBVIEW context. Attempting native interaction...")

    # Navigate and verify
    print("Navigating to Google...")
    driver.get("https://www.google.com")
    time.sleep(5)

    # The title check requires the WEBVIEW context to be active
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