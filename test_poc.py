import pytest
import time
from airtest.core.api import connect_device, stop_app, start_app
from poco.drivers.cocosjs import CocosJsPoco
from poco.exceptions import PocoException


# @pytest.fixture(scope="function")
# def poco_game():
#     # 1. Connect to your device
#     try:
#         device = connect_device("Android:///")
#     except Exception as e:
#         pytest.fail(f"Failed to connect to device. Is adb running? Error: {e}")
#
#     # 2. Start the App FIRST
#     package_name = "com.wptglobal.wptg"
#     stop_app(package_name)
#     start_app(package_name)
#
#     # 3. Wait for the app to load and stabilize
#     # A long initial wait is still required for game engines
#     print("\nWaiting 20 seconds for app to load and start Poco-SDK...")
#     time.sleep(20)
#
#     # 4. Initialize Poco with a Retry Loop (Ultimate Stability Fix)
#     max_retries = 3
#     retry_delay = 10  # Seconds to wait between connection attempts
#
#     for attempt in range(max_retries):
#         try:
#             print(f"Attempting to connect Poco driver... (Attempt {attempt + 1}/{max_retries})")
#             # We explicitly set a high timeout on the client initialization (60 seconds)
#             # and rely on the retry loop if this still fails.
#             poco = CocosJsPoco(device=device, cli_rpc_timeout=60)
#
#             # Immediately try a simple command to check for the RpcTimeoutError
#             # This triggers the 'dumpHierarchy' which was failing before
#             poco.agent.hierarchy.dump()
#             print("Poco driver connected and passed initial hierarchy test!")
#             break  # Connection successful, exit the loop
#
#         except PocoException as e:
#             if attempt < max_retries - 1:
#                 print(f"Poco connection/command failed: {e}. Retrying in {retry_delay} seconds...")
#                 time.sleep(retry_delay)
#             else:
#                 pytest.fail(
#                     f"Poco failed to connect after {max_retries} attempts. Check SDK integration and logs. Last Error: {e}")
#         except Exception as e:
#             # Catch any other unexpected error
#             pytest.fail(f"An unexpected error occurred during Poco initialization: {e}")
#
#     yield poco
#
#     # 5. Teardown
#     print("Test finished. Cleaning up.")
#     stop_app(package_name)
#
#
# # --- Your POC Test Function (No change needed here) ---
# # The test function will now benefit from the successfully connected 'poco' object.
# # ... (imports and fixture code remain the same) ...

def test_simple_login_button_click():
    poco = CocosJsPoco()

    login_button = poco("HallScene").offspring("btn_login")
    login_button.wait_for_appearance(timeout=30)
    login_button.click()

    login_node = poco("HallScene").offspring("LoginNode")

    assert login_node.wait_for_appearance(timeout=30), "Login failed: Did not find 'Login Node' element."
