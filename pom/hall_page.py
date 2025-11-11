import time

from pom.base_page import BasePage


class HallPage(BasePage):
    """Page Object for the main Hall scene."""

    # --- Locators ---
    # Locators are defined as tuples.
    MTT_BUTTON = ("HallScene", "mtt")
    NLHE_BUTTON = ("HallScene", "nlhe")
    FLASH_BUTTON = ("HallScene", "flash")
    PLO_BUTTON = ("HallScene", "plo")
    SHORT_DECK_BUTTON = ("HallScene", "short_deck")
    GLOBAL_SPINS_BUTTON = ("HallScene", "sng")

    BACK_BUTTON = ("HallScene", "HallPokerView", "backBtn")

    LOGIN_BUTTON = ("HallScene", "btn_login")
    BALANCE_ICON = ("HallScene", "gold_Panel")

    PROMO_CLOSE_BUTTON = ("HallScene", "Button_Close")

    # --- Actions ---

    def wait_for_hall_to_load(self, timeout=120):
        """Waits for the main hall elements to be visible."""
        print("Waiting for Hall scene to load...")
        self.wait_for_element(self.MTT_BUTTON, timeout=timeout)
        self.wait_for_element(self.LOGIN_BUTTON, timeout=timeout)
        print("Hall scene loaded.")

    def click_login_button(self):
        """Clicks the main login button to open the login modal."""
        print("Clicking main login button...")
        time.sleep(2)
        self.click_element(self.LOGIN_BUTTON)

    def close_promo_if_present(self):
        """Checks for a promo popup and closes it."""
        print("Checking for promo popup...")
        if self.is_element_visible(self.PROMO_CLOSE_BUTTON, timeout=10):
            print("Promo found, closing it.")
            self.click_element(self.PROMO_CLOSE_BUTTON)
        else:
            print("No promo popup found.")

    def is_balance_visible(self):
        """Checks if the user's balance is visible (login success)."""
        print("Verifying balance icon is visible...")
        return self.is_element_visible(self.BALANCE_ICON, timeout=20)

    def click_mtt(self):
        """Clicks the MTT button to open the MTT lobby."""
        print("Clicking MTT button...")
        self.click_element(self.MTT_BUTTON)

    def click_nlhe(self):
        """Clicks the NLHE button to open the NLHE lobby."""
        print("Clicking NLHE button...")
        self.click_element(self.NLHE_BUTTON)

    def click_flash(self):
        """Clicks the FLASH button to open the FLASH lobby."""
        print("Clicking FLASH button...")
        self.click_element(self.FLASH_BUTTON)

    def click_plo(self):
        """Clicks the PLO button to open the PLO lobby."""
        print("Clicking PLO button...")
        self.click_element(self.PLO_BUTTON)

    def click_shor_deck(self):
        """Clicks the SHORT DECK button to open the SHORT DECK lobby."""
        print("Clicking SHORT DECK button...")
        self.click_element(self.SHORT_DECK_BUTTON)

    def click_global_spins(self):
        """Clicks the GLOBAL SPINS button to open the GLOBAL SPINS lobby."""
        print("Clicking GLOBAL SPINS button...")
        self.click_element(self.GLOBAL_SPINS_BUTTON)

    def click_navigate_back_button(self):
        """Clicks the navigation back button to return to the hall."""
        print("Clicking navigation back button...")
        self.click_element(self.BACK_BUTTON)

