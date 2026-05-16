import pytest
from pages.dropdown_page import DropdownPage


@pytest.mark.regression
@pytest.mark.dropdown
class TestDropdown:
    """Test suite for dropdown functionality."""

    def test_page_loads(self, dropdown_page: DropdownPage):
        """Dropdown page should load successfully."""
        dropdown_page.navigate()
        assert "The Internet" in dropdown_page.get_title()

    def test_default_option_is_please_select(self, dropdown_page: DropdownPage):
        """Default selected option should be 'Please select an option'."""
        dropdown_page.navigate()
        assert "Please select" in dropdown_page.get_selected_option()

    def test_select_by_visible_text(self, dropdown_page: DropdownPage):
        """Selecting by visible text should work."""
        dropdown_page.navigate()
        dropdown_page.select_by_visible_text("Option 1")
        assert dropdown_page.get_selected_option() == "Option 1"

    def test_all_options_present(self, dropdown_page: DropdownPage):
        """All expected options should be present in dropdown."""
        dropdown_page.navigate()
        options = dropdown_page.get_all_options()
        assert "Option 1" in options
        assert "Option 2" in options

    def test_switch_between_options(self, dropdown_page: DropdownPage):
        """Should be able to switch selection from Option 1 to Option 2."""
        dropdown_page.navigate()
        dropdown_page.select_by_value("1")
        assert dropdown_page.get_selected_option() == "Option 1"
        dropdown_page.select_by_value("2")
        assert dropdown_page.get_selected_option() == "Option 2"

    @pytest.mark.parametrize(
        "value,expected,method",
        [
            ("1", "Option 1", "value"),
            ("2", "Option 2", "value"),
            ("Option 1", "Option 1", "text"),
            ("Option 2", "Option 2", "text"),
            (1, "Please select", "index"),  # Index 1 is default
            (2, "Option 1", "index"),
            (3, "Option 2", "index"),
        ],
        ids=[
            "select_by_value_1",
            "select_by_value_2",
            "select_by_text_1",
            "select_by_text_2",
            "select_by_index_default",
            "select_by_index_opt1",
            "select_by_index_opt2",
        ],
    )
    def test_select_dropdown_parametrized(
        self, dropdown_page: DropdownPage, value, expected: str, method: str
    ):
        """Parametrized dropdown selection test.
        
        Args:
            dropdown_page: DropdownPage fixture
            value: Selection value (index, text, or id)
            expected: Expected option text after selection
            method: Selection method (value, text, or index)
        """
        dropdown_page.navigate()

        if method == "value":
            dropdown_page.select_by_value(value)
        elif method == "text":
            dropdown_page.select_by_visible_text(value)
        elif method == "index":
            dropdown_page.select_by_index(value)

        assert dropdown_page.get_selected_option() == expected
