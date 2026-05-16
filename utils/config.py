import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Centralized configuration from environment variables."""

    BASE_URL: Final[str] = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
    BROWSER: Final[str] = os.getenv("BROWSER", "chrome")
    HEADLESS: Final[bool] = os.getenv("HEADLESS", "true").lower() == "true"
    IMPLICIT_WAIT: Final[int] = int(os.getenv("IMPLICIT_WAIT", 10))
    EXPLICIT_WAIT: Final[int] = int(os.getenv("EXPLICIT_WAIT", 15))
    SCREENSHOTS_DIR: Final[str] = "reports/screenshots"
