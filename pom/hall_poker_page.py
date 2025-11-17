import time

from pom.base_page import BasePage


class HallPokerPage(BasePage):
    """Page Object for the main Hall scene."""

    # --- Locators ---
    # Locators are defined as tuples.

    # TOP BAR ITEMS
    BACK_BUTTON = ("HallScene", "HallPokerView", "backBtn")
    MTT_GAME_LIST = ("HallScene", "mtt_game_list")
    CASH_GAME_LIST = ("HallScene", "HallPokerView", "view")
    GLOBAL_SPIN_LIST = ("HallScene", "panel_SNGGameList", "grid")

    # --- Actions ---

    def click_navigate_back_button(self):
        """Clicks the navigation back button to return to the hall."""
        print("Clicking navigation back button...")
        self.click_element(self.BACK_BUTTON)

    def verify_mtt_grid_loaded(self):
        """Verifies MTT list is loaded by checking prize pool text of first item"""
        print("Verifying MTT grid is loaded...")
        game_list = self.wait_for_element(self.MTT_GAME_LIST)
        assert game_list.offspring("prizepool_label").get_text() == "Prize Pool", \
            "MTT hall is not displayed"

    def verify_nlhe_grid_loaded(self):
        """Verifies NLHE list is loaded by checking game type text of first item"""
        print("Verifying NLHE grid is loaded...")
        game_list = self.wait_for_element(self.CASH_GAME_LIST)
        assert game_list.offspring("gameTypeLabel").get_text() == "NLHE", \
            "NLHE hall is not displayed"

    def verify_flash_grid_loaded(self):
        """Verifies FLASH list is loaded by checking buy-in text of first item"""
        print("Verifying FLASH grid is loaded...")
        game_list = self.wait_for_element(self.CASH_GAME_LIST)
        assert game_list.offspring("buyInTitle").get_text() == "Buy-In", \
            "FLASH hall is not displayed"

    def verify_plo_grid_loaded(self):
        """Verifies PLO list is loaded by checking buy-in text of first item"""
        print("Verifying PLO grid is loaded...")
        game_list = self.wait_for_element(self.CASH_GAME_LIST)
        text = game_list.offspring("gameTypeLabel").get_text()
        assert "PLO" in game_list.offspring("gameTypeLabel").get_text(), \
            "PLO hall is not displayed"

    def verify_short_deck_grid_loaded(self):
        """Verifies SHORT DECK list is loaded by checking game type text of first item"""
        print("Verifying SHORT DECK grid is loaded...")
        game_list = self.wait_for_element(self.CASH_GAME_LIST)
        assert game_list.offspring("gameTypeLabel").get_text() == "Short Deck", \
            "SHORT DECK hall is not displayed"

    def verify_global_spin_grid_loaded(self):
        """Verifies GLOBAL SPIN list is loaded by JACKPOT text of first item"""
        print("Verifying GLOBAL SPIN grid is loaded...")
        game_list = self.wait_for_element(self.GLOBAL_SPIN_LIST)
        assert game_list.offspring("label_WinUpTo").get_text() == "JACKPOT", \
            "GLOBAL SPIN hall is not displayed"
