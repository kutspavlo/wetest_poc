import time

from airtest.core.api import connect_device
from poco.drivers.cocosjs import CocosJsPoco


def test_simple_login_button_click():
    # connect_device("Android:///")
    poco = CocosJsPoco()

    mtt_button = poco("HallScene").offspring("mtt")
    mtt_button.wait_for_appearance(timeout=120)
    time.sleep(5)
    login_button = poco("HallScene").offspring("btn_login")
    login_button.click()

    login_node = poco("HallScene").offspring("LoginNode")
    login_node.wait_for_appearance(timeout=120)

    assert login_node.exists(), "Login failed: Did not find 'Login Node' element."