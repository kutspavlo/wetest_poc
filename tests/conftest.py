import json
from pathlib import Path

import pytest
import requests
from airtest.core.api import device, connect_device
from poco.drivers.cocosjs import CocosJsPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from enums.prod_domains import ProductionDomains

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
    response = requests.get(ProductionDomains.MAIN_PRIMARY.value, verify=False)
    response_data = response.json()
    return response_data
