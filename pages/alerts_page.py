from selenium.webdriver.common.by import By
from pages.base_page import BasePage, Locator


class AlertsPage(BasePage):
    """Page object for JavaScript alerts testing page at /javascript_alerts."""

    JS_ALERT_BTN: Locator = (By.CSS_SELECTOR, "button[onclick='jsAlert()']")
    JS_CONFIRM_BTN: Locator = (By.CSS_SELECTOR, "button[onclick='jsConfirm()']")
    JS_PROMPT_BTN: Locator = (By.CSS_SELECTOR, "button[onclick='jsPrompt()']")
    RESULT_TEXT: Locator = (By.ID, "result")
    PATH: str = "/javascript_alerts"

    def navigate(self) -> None:
        """Navigate to alerts page."""
        self.open(self.PATH)

    def trigger_js_alert(self) -> str:
        """Click JS alert button and accept alert.
        
        Returns:
            Alert text
        """
        self.click(self.JS_ALERT_BTN)
        return self.accept_alert()

    def trigger_js_confirm_accept(self) -> str:
        """Click confirm button and accept the confirmation.
        
        Returns:
            Alert text
        """
        self.click(self.JS_CONFIRM_BTN)
        return self.accept_alert()

    def trigger_js_confirm_dismiss(self) -> str:
        """Click confirm button and dismiss the confirmation.
        
        Returns:
            Alert text
        """
        self.click(self.JS_CONFIRM_BTN)
        return self.dismiss_alert()

    def trigger_js_prompt(self, input_text: str) -> str:
        """Click prompt button, type text, and accept.
        
        Args:
            input_text: Text to input in prompt
            
        Returns:
            Result text after accepting prompt
        """
        self.click(self.JS_PROMPT_BTN)
        self.type_in_alert(input_text)
        return self.get_result_text()

    def get_result_text(self) -> str:
        """Get the result text displayed on the page.
        
        Returns:
            Result message text
        """
        return self.get_text(self.RESULT_TEXT)
