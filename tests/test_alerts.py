import pytest
from pages.alerts_page import AlertsPage


@pytest.mark.regression
@pytest.mark.alert
class TestAlerts:
    """Test suite for JavaScript alerts and prompts."""

    def test_page_loads(self, alerts_page: AlertsPage):
        """Alerts page should load."""
        alerts_page.navigate()
        assert "The Internet" in alerts_page.get_title()

    def test_js_alert_accept(self, alerts_page: AlertsPage):
        """JS alert should be dismissible and show correct result."""
        alerts_page.navigate()
        alerts_page.trigger_js_alert()
        assert "You successfully clicked an alert" in alerts_page.get_result_text()

    def test_js_confirm_accept(self, alerts_page: AlertsPage):
        """Accepting JS confirm should show 'Ok' result."""
        alerts_page.navigate()
        alerts_page.trigger_js_confirm_accept()
        assert "Ok" in alerts_page.get_result_text()

    def test_js_confirm_dismiss(self, alerts_page: AlertsPage):
        """Dismissing JS confirm should show 'Cancel' result."""
        alerts_page.navigate()
        alerts_page.trigger_js_confirm_dismiss()
        assert "Cancel" in alerts_page.get_result_text()

    def test_js_prompt_with_text(self, alerts_page: AlertsPage):
        """JS prompt should capture typed input and display it."""
        alerts_page.navigate()
        alerts_page.trigger_js_prompt("Hello Google!")
        assert "Hello Google!" in alerts_page.get_result_text()

    def test_js_prompt_with_empty_input(self, alerts_page: AlertsPage):
        """JS prompt submitted empty should show empty result."""
        alerts_page.navigate()
        alerts_page.trigger_js_prompt("")
        result = alerts_page.get_result_text()
        assert result is not None

    @pytest.mark.parametrize(
        "prompt_text",
        [
            "Test Input 1",
            "Sushmitha",
            "12345",
            "Special @#$%",
            "",
        ],
        ids=["text_input", "name_input", "numeric_input", "special_chars", "empty_input"],
    )
    def test_js_prompt_parametrized(self, alerts_page: AlertsPage, prompt_text: str):
        """Parametrized prompt test — various inputs.
        
        Args:
            alerts_page: AlertsPage fixture
            prompt_text: Text to input into prompt
        """
        alerts_page.navigate()
        alerts_page.trigger_js_prompt(prompt_text)
        result = alerts_page.get_result_text()
        
        if prompt_text:
            assert prompt_text in result
        else:
            assert result is not None
