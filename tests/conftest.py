import json
import os
from pathlib import Path

import pytest
from airtest.core.api import device, connect_device
from poco.drivers.cocosjs import CocosJsPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions

APP_PACKAGE_NAME = "com.your.app.package"


@pytest.fixture(scope="session")
def test_credentials():
    """Provides test login credentials."""
    # In a real project, load this from env variables or a config file
    return {
        "email": "sonthaqa1@mailinator.com",
        "password": "Poker@1234!"
    }


@pytest.fixture(scope="function")
def cocos_poco():
    """
    Fixture to connect to the device, initialize CocosJsPoco,
    and handle setup/teardown for each test function.
    """
    # device = connect_device("Android:///")

    # Initialize Poco for the CocosJS game engine
    poco = CocosJsPoco()

    # --- Yield ---
    # Yield the driver to the test function
    yield poco

    # --- Teardown ---
    # This code runs after each test finishes
    print("Test finished. Tearing down cocos_poco fixture.")
    # stop_app(APP_PACKAGE_NAME) #cleanup


@pytest.fixture(scope="function")
def android_poco(get_device_os):
    """
    Fixture to initialize the native AndroidUiautomationPoco driver.
    It's "function" scoped to be available when needed.
    """
    # This assumes the device is already connected by the `cocos_poco` fixture
    if get_device_os == "android":
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        yield poco


@pytest.fixture(scope="function")
def get_device_os():
    """
    Fixture to detect current device OS
    """
    platform = device().platform
    return platform


@pytest.fixture(scope="session")
def production_domain_snapshot():
    base_dir = Path(__file__).parent
    file_path = base_dir / "data" / "production_domain_snapshot.json"
    with open(file_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def driver():
    # Check if we are running in CI via the wrapper
    remote_url = os.environ.get('UDT_REMOTE_URL')
    caps_json = os.environ.get('UDT_CAPS')

    if remote_url and caps_json:
        # CI Mode: Use the capabilities provided by the wrapper
        caps = json.loads(caps_json)
        options = AppiumOptions().load_capabilities(caps)
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        # Local Mode: Your existing local driver setup
        options = AppiumOptions()
        options.set_capability("platformName", "Android")
        driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)

    yield driver
    driver.quit()