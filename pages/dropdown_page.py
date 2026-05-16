from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage, Locator


class DropdownPage(BasePage):
    """Page object for dropdown testing page at /dropdown."""

    DROPDOWN: Locator = (By.ID, "dropdown")
    PATH: str = "/dropdown"

    def navigate(self) -> None:
        """Navigate to dropdown page."""
        self.open(self.PATH)

    def _get_select(self) -> Select:
        """Get Select object for dropdown element.
        
        Returns:
            Selenium Select object
        """
        el = self.driver.find_element(*self.DROPDOWN)
        return Select(el)

    def select_by_value(self, value: str) -> None:
        """Select dropdown option by value attribute.
        
        Args:
            value: Option value attribute
        """
        self._get_select().select_by_value(value)

    def select_by_visible_text(self, text: str) -> None:
        """Select dropdown option by visible text.
        
        Args:
            text: Option visible text
        """
        self._get_select().select_by_visible_text(text)

    def select_by_index(self, index: int) -> None:
        """Select dropdown option by index.
        
        Args:
            index: Zero-based option index
        """
        self._get_select().select_by_index(index)

    def get_selected_option(self) -> str:
        """Get currently selected option text.
        
        Returns:
            Selected option text
        """
        return self._get_select().first_selected_option.text

    def get_all_options(self) -> List[str]:
        """Get all available options in dropdown.
        
        Returns:
            List of option texts
        """
        return [opt.text for opt in self._get_select().options]
