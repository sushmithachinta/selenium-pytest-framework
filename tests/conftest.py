import pytest
import os
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver
from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.dropdown_page import DropdownPage
from pages.checkboxes_page import CheckboxesPage
from pages.alerts_page import AlertsPage
from pages.drag_drop_page import DragDropPage

logger = get_logger("conftest")


def pytest_addoption(parser):
    """Register custom command-line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome/firefox/edge",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run headless",
    )


@pytest.fixture(scope="function")
def driver(request) -> Generator[WebDriver, None, None]:
    """WebDriver fixture with auto-screenshot on failure.
    
    Yields:
        Configured WebDriver instance
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    drv = DriverFactory.get_driver(browser=browser, headless=headless)
    logger.info(f"Driver started for test: {request.node.name}")

    yield drv

    # Auto-screenshot on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("reports/screenshots", exist_ok=True)
        screenshot_path = f"reports/screenshots/FAILED_{request.node.name}.png"
        drv.save_screenshot(screenshot_path)
        logger.error(f"Test FAILED — screenshot: {screenshot_path}")

    drv.quit()
    logger.info(f"Driver closed for test: {request.node.name}")


# ── Page Object Fixtures ──────────────────────────────────────────
@pytest.fixture
def login_page(driver: WebDriver) -> LoginPage:
    """LoginPage fixture."""
    return LoginPage(driver)


@pytest.fixture
def dropdown_page(driver: WebDriver) -> DropdownPage:
    """DropdownPage fixture."""
    return DropdownPage(driver)


@pytest.fixture
def checkboxes_page(driver: WebDriver) -> CheckboxesPage:
    """CheckboxesPage fixture."""
    return CheckboxesPage(driver)


@pytest.fixture
def alerts_page(driver: WebDriver) -> AlertsPage:
    """AlertsPage fixture."""
    return AlertsPage(driver)


@pytest.fixture
def drag_drop_page(driver: WebDriver) -> DragDropPage:
    """DragDropPage fixture."""
    return DragDropPage(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Create test report with status for screenshot capture.
    
    This hook stores the test result so conftest can capture
    screenshots on failure.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
