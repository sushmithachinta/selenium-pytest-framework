from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Locator


class LoginPage(BasePage):
    """Page object for login page at /login."""

    # Locators
    USERNAME_INPUT: Locator = (By.ID, "username")
    PASSWORD_INPUT: Locator = (By.ID, "password")
    LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MSG: Locator = (By.CSS_SELECTOR, ".flash.success")
    ERROR_MSG: Locator = (By.CSS_SELECTOR, ".flash.error")
    LOGOUT_BUTTON: Locator = (By.CSS_SELECTOR, "a[href='/logout']")

    PATH: str = "/login"

    def navigate(self) -> None:
        """Navigate to login page."""
        self.open(self.PATH)

    def login(self, username: str, password: str) -> None:
        """Perform login with username and password.
        
        Args:
            username: User email/username
            password: User password
        """
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_success_message(self) -> str:
        """Get success message after login.
        
        Returns:
            Success message text
        """
        return self.get_text(self.SUCCESS_MSG)

    def get_error_message(self) -> str:
        """Get error message on login failure.
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MSG)

    def is_logged_in(self) -> bool:
        """Check if user is logged in by verifying logout button visibility.
        
        Returns:
            True if logged in, False otherwise
        """
        return self.is_visible(self.LOGOUT_BUTTON)

    def logout(self) -> None:
        """Logout user by clicking logout button."""
        self.click(self.LOGOUT_BUTTON)
