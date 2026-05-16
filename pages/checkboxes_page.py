from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Locator


class CheckboxesPage(BasePage):
    """Page object for checkbox testing page at /checkboxes."""

    CHECKBOX_1: Locator = (By.CSS_SELECTOR, "#checkboxes input:nth-child(1)")
    CHECKBOX_2: Locator = (By.CSS_SELECTOR, "#checkboxes input:nth-child(3)")
    PATH: str = "/checkboxes"

    def navigate(self) -> None:
        """Navigate to checkboxes page."""
        self.open(self.PATH)

    def is_checkbox1_checked(self) -> bool:
        """Check if checkbox 1 is selected.
        
        Returns:
            True if checked, False otherwise
        """
        return self.is_checked(self.CHECKBOX_1)

    def is_checkbox2_checked(self) -> bool:
        """Check if checkbox 2 is selected.
        
        Returns:
            True if checked, False otherwise
        """
        return self.is_checked(self.CHECKBOX_2)

    def check_checkbox1(self) -> None:
        """Check checkbox 1 if not already checked."""
        self.check(self.CHECKBOX_1)

    def uncheck_checkbox1(self) -> None:
        """Uncheck checkbox 1 if checked."""
        self.uncheck(self.CHECKBOX_1)

    def check_checkbox2(self) -> None:
        """Check checkbox 2 if not already checked."""
        self.check(self.CHECKBOX_2)

    def uncheck_checkbox2(self) -> None:
        """Uncheck checkbox 2 if checked."""
        self.uncheck(self.CHECKBOX_2)
