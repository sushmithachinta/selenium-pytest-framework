from typing import Literal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

BrowserType = Literal["chrome", "firefox", "edge"]


class DriverFactory:
    """Factory for creating and configuring WebDriver instances."""

    # Shared options for all browsers
    _COMMON_CHROME_ARGS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1920,1080",
        "--disable-gpu",
    ]

    @staticmethod
    def _get_chrome_options(headless: bool) -> webdriver.ChromeOptions:
        """Create and configure Chrome options.
        
        Args:
            headless: Run in headless mode
            
        Returns:
            Configured ChromeOptions
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        for arg in DriverFactory._COMMON_CHROME_ARGS:
            options.add_argument(arg)
        return options

    @staticmethod
    def _get_firefox_options(headless: bool) -> webdriver.FirefoxOptions:
        """Create and configure Firefox options.
        
        Args:
            headless: Run in headless mode
            
        Returns:
            Configured FirefoxOptions
        """
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return options

    @staticmethod
    def _get_edge_options(headless: bool) -> webdriver.EdgeOptions:
        """Create and configure Edge options.
        
        Args:
            headless: Run in headless mode
            
        Returns:
            Configured EdgeOptions
        """
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        return options

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None) -> webdriver.Remote:
        """Create and return a WebDriver instance.
        
        Args:
            browser: Browser type (chrome/firefox/edge). Defaults to Config.BROWSER
            headless: Run in headless mode. Defaults to Config.HEADLESS
            
        Returns:
            Configured WebDriver instance
            
        Raises:
            ValueError: If unsupported browser is specified
        """
        browser = (browser or Config.BROWSER).lower()
        headless = headless if headless is not None else Config.HEADLESS

        logger.info(f"Launching browser: {browser} | headless: {headless}")

        driver = None
        
        if browser == "chrome":
            options = DriverFactory._get_chrome_options(headless)
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )

        elif browser == "firefox":
            options = DriverFactory._get_firefox_options(headless)
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )

        elif browser == "edge":
            options = DriverFactory._get_edge_options(headless)
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )

        else:
            raise ValueError(
                f"Unsupported browser: {browser}. "
                f"Supported browsers: chrome, firefox, edge"
            )

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.maximize_window()
        logger.info(f"Browser launched successfully: {browser}")
        
        return driver
