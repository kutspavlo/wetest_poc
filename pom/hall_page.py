from pom.base_page import BasePage


class HallPage(BasePage):
    """Page Object for the main Hall scene."""

    # --- Locators ---
    # Locators are defined as tuples.
    MTT_BUTTON = ("HallScene", "mtt")
    LOGIN_BUTTON = ("HallScene", "btn_login")
    PROMO_CLOSE_BUTTON = ("HallScene", "Button_Close")
    BALANCE_ICON = ("HallScene", "gold_Panel")

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