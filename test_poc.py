import time

from airtest.core.api import connect_device, text
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
    time.sleep(5)

    assert login_node.exists(), "Login failed: Did not find 'Login Node' element."

    # 2. Define the input fields
    email_field = poco("HallScene").offspring("username_input").offspring("text")
    password_field = poco("HallScene").offspring("password_input").offspring("text")

    # 3. Wait for email field, THEN click and type
    email_field.wait_for_appearance(timeout=30)
    email_field.click()
    text("dreambel@icloud.com")

    # 4. Wait for password field, THEN click and type
    password_field.wait_for_appearance(timeout=30)
    password_field.click()
    text("Pavelrew22011991!")
