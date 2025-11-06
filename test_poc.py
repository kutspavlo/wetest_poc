import time

from airtest.core.api import connect_device
from poco.drivers.cocosjs import CocosJsPoco
from adb_util import adb_type_text, adb_press_enter


def test_simple_login_button_click():
    connect_device("Android:///")
    poco = CocosJsPoco()

    mtt_button = poco("HallScene").offspring("mtt")
    mtt_button.wait_for_appearance(timeout=120)
    time.sleep(5)
    login_button = poco("HallScene").offspring("btn_login")
    login_button.click()

    login_node = poco("HallScene").offspring("LoginNode")
    login_node.wait_for_appearance(timeout=120)
    time.sleep(15)

    assert login_node.exists(), "Login failed: Did not find 'Login Node' element."

    # 6. Now, try to interact with the fields
    email_field = poco("HallScene").offspring("username_input").offspring("bg")
    password_field = poco("HallScene").offspring("password_input").offspring("bg")

    # --- Human-Like Email Click ---
    email_field.wait_for_appearance(timeout=10)
    email_field.click()
    time.sleep(2)
    adb_type_text("dreambel@icloud.com")
    adb_press_enter()

    # --- Human-Like Password Click ---
    password_field.wait_for_appearance(timeout=10)
    password_field.click()
    time.sleep(2)
    adb_type_text("Pavelrew22011991")
    time.sleep(2)
    adb_press_enter()


    captcha_checkbox = poco("HallScene").offspring("Captcha")
    captcha_checkbox.click()
    time.sleep(10)

    login_button_confirm = poco("HallScene").offspring("login_button")
    login_button_confirm.click()
    time.sleep(20)