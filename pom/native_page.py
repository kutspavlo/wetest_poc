from pom.base_page import BasePage


class NativePage(BasePage):
    """Page Object for native Android UI elements."""

    # --- Locators ---
    NAVIGATE_UP_BUTTON = ("android.widget.FrameLayout", "android.widget.LinearLayout", "Navigate up")

    def __init__(self, poco):
        # This class expects the android_poco driver
        super().__init__(poco)

    def click_navigate_up(self):
        """Clicks the native 'Navigate up' button."""
        print("Clicking native 'Navigate up' button...")
        self.click_element(self.NAVIGATE_UP_BUTTON, timeout=15)
