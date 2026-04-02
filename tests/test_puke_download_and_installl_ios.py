# -*- coding: UTF-8 -*-
import os
import time
import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions


@pytest.fixture(scope="function")
def driver():
    udid = os.getenv("IOS_SERIAL")
    wda_url = os.getenv("WDA_HOST")

    print(f"\nTarget UDID: {udid}")

    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'
    options.device_name = 'iOS'

    # Launch Safari purely as a native app
    options.bundle_id = 'com.apple.mobilesafari'
    options.udid = udid

    if wda_url:
        options.set_capability('webDriverAgentUrl', wda_url)
        options.set_capability('usePrebuiltWDA', True)

    options.new_command_timeout = 600
    options.auto_accept_alerts = True

    print("Initializing Appium driver...")
    driver_instance = webdriver.Remote(
        command_executor="http://localhost:4723/wd/hub",
        options=options
    )

    yield driver_instance
    driver_instance.quit()


def test_safari_google_search(driver):
    print("Launching Safari as Native App...")

    # Wait for Safari to open
    time.sleep(5)

    print("Locating the URL bar...")
    # On iOS Safari, the URL bar is identified as a button initially (reading "Address")
    try:
        url_button = driver.find_element(by='name', value='URL')
    except:
        try:
            url_button = driver.find_element(by='name', value='Address')
        except:
            # Fallback for different iOS versions
            url_button = driver.find_element(by='accessibility id', value='TabBarItemTitle')

    # Tap the URL bar to bring up the keyboard
    url_button.click()
    time.sleep(2)

    print("Typing URL...")
    # Once clicked, it becomes a text field
    url_field = driver.find_element(by='class name', value='XCUIElementTypeTextField')
    url_field.send_keys("https://landing.koh2de.com/zh-CN/invite-bonus-zh-hans-cn?referralCode=UQP1PH")
    time.sleep(1)

    print("Hitting Go/Enter...")
    # Click the "Go" button on the iOS keyboard
    driver.find_element(by='name', value='Go').click()

    # Wait for page to load
    print("Waiting for page load...")
    time.sleep(6)

    print("Hitting Download button...")
    download_button = driver.find_element(by='accessibility id', value='下载 WPT Global Puke')
    download_button.click()
    time.sleep(7)

    print("Hitting AppStore Download button...")
    appstore_download_button = driver.find_element(by='accessibility id', value='获取')
    appstore_download_button.click()
    time.sleep(30)

    print("Waiting for installation to complete via App State...")
    bundle_id = "com.wptglobal.wptgpuke"
    timeout = 180  # Max wait time in seconds
    poll_interval = 5
    elapsed_time = 0

    # Loop until the app state is no longer 0 (Not Installed)
    while driver.query_app_state(bundle_id) == 0:
        if elapsed_time >= timeout:
            raise Exception(f"App {bundle_id} failed to install within {timeout} seconds.")
        time.sleep(poll_interval)
        elapsed_time += poll_interval

    print("Install finished! Starting Puke App...")
    driver.terminate_app(bundle_id)
    driver.activate_app(bundle_id)
    time.sleep(15)


if __name__ == '__main__':
    upload_dir = os.getenv("UPLOADDIR", ".")
    report_path = os.path.join(upload_dir, "report.xml")

    pytest.main([
        "-v",
        "-s",
        f"--junitxml={report_path}",
        __file__
    ])