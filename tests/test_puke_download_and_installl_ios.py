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

    print("Hitting Download button...")
    # Click the "Go" button on the iOS keyboard
    download_button = driver.find_element(by='accessibility id', value='下载 WPT Global Puke')


if __name__ == '__main__':
    upload_dir = os.getenv("UPLOADDIR", ".")
    report_path = os.path.join(upload_dir, "report.xml")

    pytest.main([
        "-v",
        "-s",
        f"--junitxml={report_path}",
        __file__
    ])
