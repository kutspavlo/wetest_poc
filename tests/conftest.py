import pytest
from airtest.core.api import connect_device, stop_app, clear_app
from poco.drivers.cocosjs import CocosJsPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# Define the package name of your app
APP_PACKAGE_NAME = "com.your.app.package"


@pytest.fixture(scope="session")
def test_credentials():
    """Provides test login credentials."""
    # In a real project, load this from env variables or a config file
    return {
        "email": "dreambel@icloud.com",
        "password": "Pavelrew22011991"
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
def android_poco():
    """
    Fixture to initialize the native AndroidUiautomationPoco driver.
    It's "function" scoped to be available when needed.
    """
    # This assumes the device is already connected by the `cocos_poco` fixture
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    yield poco
