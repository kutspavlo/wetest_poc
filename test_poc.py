from airtest.core.api import connect_device
from poco.drivers.cocosjs import CocosJsPoco
from poco.exceptions import PocoException

def test_simple_login_button_click():
    # connect_device("Android:///")
    poco = CocosJsPoco()

    login_button = poco("HallScene").offspring("btn_login").offspring("lbl_login")
    login_button.wait_for_appearance(timeout=120)
    login_button.click()

    login_node = poco("HallScene").offspring("LoginNode")
    login_button.wait_for_appearance(timeout=120)

    assert login_node, "Login failed: Did not find 'Login Node' element."
