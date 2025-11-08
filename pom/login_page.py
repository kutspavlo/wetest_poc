from pom.base_page import BasePage
from utils.adb_utils import adb_type_text, adb_press_enter
import time


class LoginPage(BasePage):
    """Page Object for the Login modal/node."""

    # --- Locators ---
    LOGIN_NODE = ("HallScene", "LoginNode")
    EMAIL_FIELD = ("HallScene", "username_input", "bg")
    PASSWORD_FIELD = ("HallScene", "password_input", "bg")
    CAPTCHA_CHECKBOX = ("HallScene", "Captcha")
    CONFIRM_LOGIN_BUTTON = ("HallScene", "login_button")  # Assumed, same as original

    # --- Actions ---

    def wait_for_login_modal(self):
        """Waits for the login modal to appear."""
        print("Waiting for login modal to appear...")
        self.wait_for_element(self.LOGIN_NODE, timeout=120)
        print("Login modal is visible.")

    def enter_email(self, email):
        """Enters text into the email field."""
        print(f"Entering email: {email}")
        self.click_element(self.EMAIL_FIELD, timeout=10)
        # Using ADB for text entry as in the original script
        adb_type_text(email)
        adb_press_enter()

    def enter_password(self, password):
        """Enters text into the password field."""
        print("Entering password...")
        self.click_element(self.PASSWORD_FIELD, timeout=10)
        adb_type_text(password)
        adb_press_enter()

    def click_captcha(self):
        """
        Clicks the captcha checkbox.
        NOTE: Real automation of captcha is complex/not recommended.
        This assumes clicking it is enough, or a dev build disables it.
        """
        print("Clicking captcha checkbox...")
        self.click_element(self.CAPTCHA_CHECKBOX)
        # The long wait for manual solving is moved to the test logic
        # if it's truly necessary. Here, we just click.

    def click_confirm_login(self):
        """Clicks the final login button on the modal."""
        print("Clicking confirm login button...")
        self.click_element(self.CONFIRM_LOGIN_BUTTON)

    def login_with_credentials(self, email, password):
        """High-level method to perform a full login."""
        self.wait_for_login_modal()
        self.enter_email(email)
        self.enter_password(password)
        self.click_captcha()
        time.sleep(10)
        self.click_confirm_login()