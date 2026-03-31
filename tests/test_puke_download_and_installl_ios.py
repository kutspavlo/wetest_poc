# -*- coding: UTF-8 -*-
import os
import time
import pytest
from appium import webdriver


@pytest.fixture(scope="function")
def driver():
    print('\n--- WeTest Environment Variables Debug ---')
    # This will print to your WeTest logs so we can see EXACTLY what variables they provide
    for key, value in os.environ.items():
        if any(x in key.upper() for x in ['IOS', 'WDA', 'UDID', 'DEVICE', 'PORT']):
            print(f"{key}: {value}")
    print('------------------------------------------')

    # Fetch WeTest dynamic variables
    udid = os.getenv("IOS_SERIAL")
    wda_ip = os.getenv("WDA_SERVER_IP")
    wda_port = os.getenv("WDA_SERVER_PORT")

    # We remove the safeguard. If WeTest doesn't provide the IP, we want to know.
    wda_url = f"http://{wda_ip}:{wda_port}/"

    desired_caps = {
        'platformName': 'iOS',
        'automationName': 'XCUITest',
        'deviceName': 'iOS',
        'newCommandTimeout': 600,

        # Treat Safari as a standard Native iOS App to bypass Xcode WebKit checks
        'bundleId': 'com.apple.mobilesafari',

        # Cloud Environment variables injected by WeTest
        'udid': udid,
        'webDriverAgentUrl': wda_url,
        'usePrebuiltWDA': True,

        'autoAcceptAlerts': True
    }

    print(f"\nInitializing driver with WDA URL: {wda_url}")
    driver_instance = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    yield driver_instance

    print('\nTearing down driver...')
    driver_instance.quit()


def test_safari_google_search(driver):
    print('Starting Safari native launch...')

    # Because we used bundleId, Safari launches natively.
    # We must wait a moment for the app to open.
    time.sleep(3)

    print('Available Contexts:', driver.contexts)

    # Switch from NATIVE_APP to the WEBVIEW context so we can use standard web commands
    webview_context = None
    for context in driver.contexts:
        if 'WEBVIEW' in context:
            webview_context = context
            break

    if webview_context:
        print(f"Switching to context: {webview_context}")
        driver.switch_to.context(webview_context)
    else:
        print("WARNING: Could not find WEBVIEW context. Trying native navigation...")

    # Navigate and verify
    driver.get("https://www.google.com")
    time.sleep(4)

    assert "Google" in driver.title, f"Expected 'Google' in title, but got: {driver.title}"
    print('Successfully validated Safari navigation.')


if __name__ == '__main__':
    upload_dir = os.getenv("UPLOADDIR", ".")
    report_path = os.path.join(upload_dir, "report.xml")

    pytest.main([
        "-v",
        "-s",  # Crucial: Ensures our print() statements appear in the WeTest console logs
        f"--junitxml={report_path}",
        __file__
    ])