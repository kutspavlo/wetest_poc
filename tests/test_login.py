import pytest
from pom.hall_page import HallPage
from pom.login_page import LoginPage
from pom.native_page import NativePage


@pytest.mark.login
def test_user_login(cocos_poco, android_poco, test_credentials):
    """
    Test case for a successful user login.

    Fixtures:
    - cocos_poco: Provides the initialized CocosJS driver.
    - android_poco: Provides the initialized Android UIAutomation driver.
    - test_credentials: Provides the email and password.
    """

    # 1. Initialize Page Objects with their respective drivers
    hall_page = HallPage(cocos_poco)
    login_page = LoginPage(cocos_poco)
    native_page = NativePage(android_poco)

    # 2. Wait for the app's main hall to load
    hall_page.wait_for_hall_to_load()

    # 3. Navigate to the login screen
    hall_page.click_login_button()

    # 4. Perform the login
    login_page.login_with_credentials(
        test_credentials["email"],
        test_credentials["password"]
    )

    # 5. Handle the native "Navigate Up" action
    native_page.click_navigate_up()

    # 6. Handle post-login popups
    hall_page.close_promo_if_present()

    # 7. Final Assertion: Verify login was successful
    assert hall_page.is_balance_visible(), "Login failed: Balance icon was not found."

    # 8. Navigate and varify various game types
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
