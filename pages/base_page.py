from typing import List, Optional, Tuple
import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    NoAlertPresentException,
)
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

Locator = Tuple[By, str]


class BasePage:
    """Base class for all page objects providing reusable WebDriver actions."""

    def __init__(self, driver: WebDriver):
        """Initialize page object with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.actions: ActionChains = ActionChains(driver)

    # ── Navigation ────────────────────────────────────────────
    def open(self, path: str = "") -> None:
        """Navigate to a URL path.
        
        Args:
            path: URL path relative to BASE_URL (e.g., "/login")
        """
        url = f"{Config.BASE_URL}{path}"
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_title(self) -> str:
        """Get current page title.
        
        Returns:
            Page title string
        """
        return self.driver.title

    def get_current_url(self) -> str:
        """Get current page URL.
        
        Returns:
            Current URL string
        """
        return self.driver.current_url

    # ── Element interactions ──────────────────────────────────
    def click(self, locator: Locator) -> None:
        """Click an element.
        
        Args:
            locator: Element locator tuple (By, value)
            
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        logger.info(f"Clicking: {locator}")
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException as e:
            raise TimeoutException(
                f"Element {locator} not clickable within {Config.EXPLICIT_WAIT}s"
            ) from e

    def type_text(self, locator: Locator, text: str) -> None:
        """Type text into an input field.
        
        Args:
            locator: Element locator tuple
            text: Text to type
            
        Raises:
            TimeoutException: If element not visible within timeout
        """
        logger.info(f"Typing '{text}' into: {locator}")
        try:
            el = self.wait.until(EC.visibility_of_element_located(locator))
            el.clear()
            el.send_keys(text)
        except TimeoutException as e:
            raise TimeoutException(
                f"Element {locator} not visible within {Config.EXPLICIT_WAIT}s"
            ) from e

    def get_text(self, locator: Locator) -> str:
        """Get text content from an element.
        
        Args:
            locator: Element locator tuple
            
        Returns:
            Element text content
            
        Raises:
            TimeoutException: If element not visible within timeout
        """
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).text
        except TimeoutException as e:
            raise TimeoutException(
                f"Element {locator} not visible within {Config.EXPLICIT_WAIT}s"
            ) from e

    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """Get element attribute value.
        
        Args:
            locator: Element locator tuple
            attribute: Attribute name
            
        Returns:
            Attribute value or None if not found
        """
        try:
            el = self.wait.until(EC.presence_of_element_located(locator))
            return el.get_attribute(attribute)
        except TimeoutException as e:
            raise TimeoutException(
                f"Element {locator} not present within {Config.EXPLICIT_WAIT}s"
            ) from e

    def is_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """Check if element is visible.
        
        Args:
            locator: Element locator tuple
            timeout: Custom timeout in seconds (uses Config.EXPLICIT_WAIT if None)
            
        Returns:
            True if visible, False otherwise
        """
        wait_timeout = timeout or Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            logger.debug(f"Element {locator} not visible within {wait_timeout}s")
            return False

    def is_present(self, locator: Locator) -> bool:
        """Check if element is present in DOM.
        
        Args:
            locator: Element locator tuple
            
        Returns:
            True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            logger.debug(f"Element {locator} not present")
            return False

    def get_all_elements(self, locator: Locator) -> List[WebElement]:
        """Get all matching elements.
        
        Args:
            locator: Element locator tuple
            
        Returns:
            List of WebElement objects
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ── Checkbox / Select helpers ─────────────────────────────
    def is_checked(self, locator: Locator) -> bool:
        """Check if checkbox/radio is selected.
        
        Args:
            locator: Element locator tuple
            
        Returns:
            True if selected, False otherwise
        """
        el = self.wait.until(EC.presence_of_element_located(locator))
        return el.is_selected()

    def check(self, locator: Locator) -> None:
        """Check a checkbox or radio button if not already checked.
        
        Args:
            locator: Element locator tuple
        """
        el = self.wait.until(EC.element_to_be_clickable(locator))
        if not el.is_selected():
            el.click()
            logger.info(f"Checked: {locator}")

    def uncheck(self, locator: Locator) -> None:
        """Uncheck a checkbox if checked.
        
        Args:
            locator: Element locator tuple
        """
        el = self.wait.until(EC.element_to_be_clickable(locator))
        if el.is_selected():
            el.click()
            logger.info(f"Unchecked: {locator}")

    # ── Alerts ────────────────────────────────────────────────
    def accept_alert(self) -> str:
        """Accept a JavaScript alert.
        
        Returns:
            Alert text content
            
        Raises:
            TimeoutException: If alert not present within timeout
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            logger.info(f"Alert accepted. Text: {text}")
            return text
        except TimeoutException as e:
            raise TimeoutException("No alert present") from e

    def dismiss_alert(self) -> str:
        """Dismiss (cancel) a JavaScript alert.
        
        Returns:
            Alert text content
            
        Raises:
            TimeoutException: If alert not present within timeout
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.dismiss()
            logger.info(f"Alert dismissed. Text: {text}")
            return text
        except TimeoutException as e:
            raise TimeoutException("No alert present") from e

    def type_in_alert(self, text: str) -> None:
        """Type text into a JavaScript prompt alert and accept.
        
        Args:
            text: Text to type into alert
            
        Raises:
            TimeoutException: If alert not present within timeout
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert.send_keys(text)
            alert.accept()
            logger.info(f"Typed '{text}' in alert and accepted")
        except TimeoutException as e:
            raise TimeoutException("No alert present") from e

    # ── Drag & Drop ───────────────────────────────────────────
    def drag_and_drop(self, source_locator: Locator, target_locator: Locator) -> None:
        """Drag element from source to target location.
        
        Args:
            source_locator: Source element locator tuple
            target_locator: Target element locator tuple
        """
        source = self.wait.until(EC.presence_of_element_located(source_locator))
        target = self.wait.until(EC.presence_of_element_located(target_locator))
        self.actions.drag_and_drop(source, target).perform()
        logger.info(f"Dragged {source_locator} → {target_locator}")

    # ── Screenshot ────────────────────────────────────────────
    def take_screenshot(self, name: str) -> str:
        """Take a screenshot of the current page.
        
        Args:
            name: Screenshot filename (without extension)
            
        Returns:
            Full path to saved screenshot
        """
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        path = f"{Config.SCREENSHOTS_DIR}/{name}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved: {path}")
        return path

    # ── Waits ─────────────────────────────────────────────────
    def wait_for_text(
        self, locator: Locator, text: str, timeout: Optional[int] = None
    ) -> None:
        """Wait for element to contain specific text.
        
        Args:
            locator: Element locator tuple
            text: Expected text content
            timeout: Custom timeout in seconds (uses Config.EXPLICIT_WAIT if None)
            
        Raises:
            TimeoutException: If text not found within timeout
        """
        wait_timeout = timeout or Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            logger.info(f"Text '{text}' found in {locator}")
        except TimeoutException as e:
            raise TimeoutException(
                f"Text '{text}' not found in {locator} within {wait_timeout}s"
            ) from e

    def wait_for_url(self, url_fragment: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to contain specific fragment.
        
        Args:
            url_fragment: URL fragment to wait for
            timeout: Custom timeout in seconds (uses Config.EXPLICIT_WAIT if None)
            
        Raises:
            TimeoutException: If URL fragment not found within timeout
        """
        wait_timeout = timeout or Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                EC.url_contains(url_fragment)
            )
            logger.info(f"URL contains: {url_fragment}")
        except TimeoutException as e:
            raise TimeoutException(
                f"URL does not contain '{url_fragment}' within {wait_timeout}s"
            ) from e
