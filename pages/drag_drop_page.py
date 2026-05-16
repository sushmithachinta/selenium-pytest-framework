from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Locator


class DragDropPage(BasePage):
    """Page object for drag and drop testing page at /drag_and_drop."""

    COLUMN_A: Locator = (By.ID, "column-a")
    COLUMN_B: Locator = (By.ID, "column-b")
    PATH: str = "/drag_and_drop"

    def navigate(self) -> None:
        """Navigate to drag and drop page."""
        self.open(self.PATH)

    def get_column_a_text(self) -> str:
        """Get text content of column A.
        
        Returns:
            Column A text
        """
        return self.get_text(self.COLUMN_A)

    def get_column_b_text(self) -> str:
        """Get text content of column B.
        
        Returns:
            Column B text
        """
        return self.get_text(self.COLUMN_B)

    def drag_a_to_b(self) -> None:
        """Drag column A to column B position."""
        self.drag_and_drop(self.COLUMN_A, self.COLUMN_B)

    def drag_b_to_a(self) -> None:
        """Drag column B to column A position."""
        self.drag_and_drop(self.COLUMN_B, self.COLUMN_A)
