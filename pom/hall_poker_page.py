import time

from pom.base_page import BasePage
from utils.string_utils import is_integer_string
from utils.string_utils import is_matching_pattern


class HallPokerPage(BasePage):
    """Page Object for the main Hall scene."""

    # --- Locators ---
    # Locators are defined as tuples.

    # TOP BAR ITEMS
    BACK_BUTTON = ("HallScene", "HallPokerView", "backBtn")
    MTT_GAME_LIST = ("HallScene", "mtt_game_list")
    CASH_GAME_LIST = ("HallScene", "HallPokerView", "view", ">content")
    GLOBAL_SPIN_LIST = ("HallScene", "panel_SNGGameList", "grid")

    # ROOM LIST
    CASH_GAME_ROOM_LIST = ("HallScene", "HallPokerView", "CashGameRoomList", "view", ">content")

    # TECH ELEMENTS
    CASH_GAME_SCROLL = ("HallScene", "HallPokerView", "container")

    # GAME TYPE PATTERNS
    NLHE_REGULAR_PATTERN = r'^HL\d{4}$'
    NLHE_BOMB_POTS_PATTERN = r'^HLB\d{4}$'

    #CASH TABLE
    SEATS = ("gameContainer", "view", "page1", "seatPanel", "Seat")

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

    def find_and_click_cash_game_by_small_blind_limit(self, small_blind, max_scroll_attempts=10):
        """Finds CASH game by small blind limit (i.e 0.02 0.02$/0.05$) """
        # TO DO: Cover edge case whek game element hides behind bottom bar (click leads to cashier)
        game_list = self.wait_for_element(self.CASH_GAME_LIST)
        game_grid_raw = game_list.children()
        print("Filtering non-game elements (scrolls, loaders, etc.)")
        game_grid = [
            game for game in game_grid_raw
            if is_integer_string(game.get_name())
        ]

        scroll_bar = self.wait_for_element(self.CASH_GAME_SCROLL)

        print("Iterating with scroll to find a game with desired small blind value")
        attempts = 0
        while attempts < max_scroll_attempts:
            for game in game_grid:
                if game.offspring("stakeLabel").get_text().startswith("$" + str(small_blind)):
                    time.sleep(2)
                    game.offspring("content").click()
                    print("Game found, clicking")
                    return

            scroll_bar.scroll("vertical", 0.7, 2.0)
            attempts += 1

    def find_by_pattern_and_click_table_with_seats(self, pattern):
        """Find and click table with available seats and matches game type pattern"""
        # TO DO: implement scroll if needed

        game_list = self.wait_for_element(self.CASH_GAME_ROOM_LIST)
        game_grid_raw = game_list.children()
        print("Filtering non-game elements (scrolls, loaders, etc.)")
        game_grid = [
            game for game in game_grid_raw
            if is_integer_string(game.get_name())
        ]

        for game in game_grid:
            if (game.offspring("playerCountLabel").get_text() != "8/8") & (
                    is_matching_pattern(game.offspring("roomName").get_text(), pattern)):
                game.offspring("content").click()
                return

    def join_cash_table_on_available_seat(self):
        """Find and seat on available cash table place"""
        seats = self.wait_for_element(self.SEATS)
        for seat in seats:
            if not seat.offspring("roleName_text_forRemark").exists():
                seat.offspring("button").click()
                return
