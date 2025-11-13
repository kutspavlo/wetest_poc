import pytest
from pom.hall_page import HallPage
from pom.login_page import LoginPage
from pom.native_page import NativePage


@pytest.mark.login
def test_games_navigation(cocos_poco, android_poco, test_credentials, get_device_os):

    hall_page = HallPage(cocos_poco)
    login_page = LoginPage(cocos_poco)
    native_page = NativePage(android_poco)

    hall_page.wait_for_hall_to_load()
    hall_page.click_login_button()

    login_page.login_with_credentials(
        test_credentials["email"],
        test_credentials["password"]
    )

    if get_device_os == "android":
        native_page.click_navigate_up()

    hall_page.close_promo_if_present()

    assert hall_page.is_balance_visible(), "Login failed: Balance icon was not found."

    hall_page.click_mtt()
    hall_page.click_navigate_back_button()
    hall_page.click_nlhe()
    hall_page.click_navigate_back_button()
    hall_page.click_flash()
    hall_page.click_navigate_back_button()
    hall_page.click_plo()
    hall_page.click_navigate_back_button()
    hall_page.click_shor_deck()
    hall_page.click_navigate_back_button()
    hall_page.click_global_spins()
    hall_page.click_navigate_back_button()
