import pytest
from pages.login_page import LoginPage

# Valid credentials for the-internet.herokuapp.com
VALID_USER = "tomsmith"
VALID_PASS = "SuperSecretPassword!"


@pytest.mark.smoke
@pytest.mark.login
class TestLogin:
    """Test suite for login functionality."""

    def test_valid_login_succeeds(self, login_page: LoginPage):
        """Valid credentials should log in and show success message."""
        login_page.navigate()
        login_page.login(VALID_USER, VALID_PASS)

        assert login_page.is_logged_in(), "Logout button not visible — login failed"
        assert "You logged into a secure area!" in login_page.get_success_message()

    def test_logout_after_login(self, login_page: LoginPage):
        """User should be able to log out after logging in."""
        login_page.navigate()
        login_page.login(VALID_USER, VALID_PASS)
        assert login_page.is_logged_in()

        login_page.logout()
        assert "You logged out of the secure area!" in login_page.get_success_message()
        assert not login_page.is_logged_in()

    def test_login_page_title(self, login_page: LoginPage):
        """Login page should have correct title."""
        login_page.navigate()
        assert "The Internet" in login_page.get_title()

    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            (VALID_USER, "WrongPassword", "Your password is invalid!"),
            ("wronguser", VALID_PASS, "Your username is invalid!"),
            ("", "", ""),
            (VALID_USER, "", ""),
            ("", VALID_PASS, ""),
        ],
        ids=[
            "invalid_password",
            "invalid_username",
            "empty_credentials",
            "empty_password",
            "empty_username",
        ],
    )
    def test_login_errors(
        self, login_page: LoginPage, username: str, password: str, expected_error: str
    ):
        """Parametrized test: various login error scenarios.
        
        Args:
            login_page: LoginPage fixture
            username: Test username
            password: Test password
            expected_error: Expected error message (may be empty for generic error)
        """
        login_page.navigate()
        login_page.login(username, password)

        assert not login_page.is_logged_in(), "User should not be logged in"
        error_msg = login_page.get_error_message()
        
        if expected_error:
            assert expected_error in error_msg
        else:
            assert "invalid" in error_msg.lower() or error_msg

    def test_login_redirects_to_secure_area(self, driver):
        """After login, URL should contain /secure."""
        page = LoginPage(driver)
        page.navigate()
        page.login(VALID_USER, VALID_PASS)
        assert "/secure" in page.get_current_url()

    @pytest.mark.parametrize("username,password,expected_error", [
        ("tomsmith",   "wrongpass",   "Your password is invalid!"),
        ("wronguser",  "SuperSecretPassword!", "Your username is invalid!"),
        ("",           "",            "invalid"),
    ])
    def test_invalid_login_parametrized(self, driver, username, password, expected_error):
        """Parametrized test for multiple invalid login combinations."""
        page = LoginPage(driver)
        page.navigate()
        page.login(username, password)

        assert not page.is_logged_in()
        assert expected_error.lower() in page.get_error_message().lower()
