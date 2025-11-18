import pytest
from pom.hall_page import HallPage
from pom.hall_poker_page import HallPokerPage
from pom.login_page import LoginPage
from pom.native_page import NativePage


@pytest.mark.login
def test_user_login(cocos_poco, android_poco, test_credentials, get_device_os):
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
    if get_device_os == "android":
        native_page.click_navigate_up()

    # 6. Handle post-login popups
    hall_page.close_promo_if_present()

    # 7. Final Assertion: Verify login was successful
    assert hall_page.is_balance_visible(), "Login failed: Balance icon was not found."


@pytest.mark.login
def test_poker_navigation(cocos_poco):
    """
    Test case for a successful poker games navigation.

    Fixtures:
    - cocos_poco: Provides the initialized CocosJS driver.
    """

    # 1. Initialize Page Objects with their respective drivers
    hall_page = HallPage(cocos_poco)
    hall_poker_page = HallPokerPage(cocos_poco)

    # 2. Navigate to MTT grid and verify it appears
    hall_page.click_mtt()
    hall_poker_page.verify_mtt_grid_loaded()
    hall_poker_page.click_navigate_back_button()

    # 3. Navigate to NLHE grid and verify it appears
    hall_page.click_nlhe()
    hall_poker_page.verify_nlhe_grid_loaded()
    hall_poker_page.click_navigate_back_button()

    # 4. Navigate to FLASH grid and verify it appears
    hall_page.click_flash()
    hall_poker_page.verify_flash_grid_loaded()
    hall_poker_page.click_navigate_back_button()

    # 5. Navigate to PLO grid and verify it appears
    hall_page.click_plo()
    hall_poker_page.verify_plo_grid_loaded()
    hall_poker_page.click_navigate_back_button()

    # 6. Navigate to SHORT DECK grid and verify it appears
    hall_page.click_short_deck()
    hall_poker_page.verify_short_deck_grid_loaded()
    hall_poker_page.click_navigate_back_button()

    # 6. Navigate to GLOBAL SPINS grid and verify it appears
    hall_page.click_global_spins()
    hall_poker_page.verify_global_spin_grid_loaded()
    hall_poker_page.click_navigate_back_button()


def test_hlhe_table(cocos_poco):
    """
        Test case for a successful NLHE game joining.

        Fixtures:
        - cocos_poco: Provides the initialized CocosJS driver.
        """

    hall_page = HallPage(cocos_poco)
    hall_poker_page = HallPokerPage(cocos_poco)

    hall_page.click_nlhe()
    hall_poker_page.find_and_click_cash_game_by_small_blind_limit(1)
    hall_poker_page.find_by_pattern_and_click_table_with_seats(hall_poker_page.NLHE_REGULAR_PATTERN)
    hall_poker_page.join_cash_table_on_available_seat()
