import pytest
from pages.checkboxes_page import CheckboxesPage


@pytest.mark.regression
@pytest.mark.checkbox
class TestCheckboxes:
    """Test suite for checkbox functionality."""

    def test_page_loads(self, checkboxes_page: CheckboxesPage):
        """Checkboxes page should load."""
        checkboxes_page.navigate()
        assert "The Internet" in checkboxes_page.get_title()

    def test_checkbox1_default_unchecked(self, checkboxes_page: CheckboxesPage):
        """Checkbox 1 should be unchecked by default."""
        checkboxes_page.navigate()
        assert not checkboxes_page.is_checkbox1_checked()

    def test_checkbox2_default_checked(self, checkboxes_page: CheckboxesPage):
        """Checkbox 2 should be checked by default."""
        checkboxes_page.navigate()
        assert checkboxes_page.is_checkbox2_checked()

    def test_check_checkbox1(self, checkboxes_page: CheckboxesPage):
        """Should be able to check Checkbox 1."""
        checkboxes_page.navigate()
        checkboxes_page.check_checkbox1()
        assert checkboxes_page.is_checkbox1_checked()

    def test_uncheck_checkbox2(self, checkboxes_page: CheckboxesPage):
        """Should be able to uncheck Checkbox 2."""
        checkboxes_page.navigate()
        checkboxes_page.uncheck_checkbox2()
        assert not checkboxes_page.is_checkbox2_checked()

    def test_check_then_uncheck_checkbox1(self, checkboxes_page: CheckboxesPage):
        """Check and then uncheck Checkbox 1 — should end unchecked."""
        checkboxes_page.navigate()
        checkboxes_page.check_checkbox1()
        assert checkboxes_page.is_checkbox1_checked()
        checkboxes_page.uncheck_checkbox1()
        assert not checkboxes_page.is_checkbox1_checked()

    def test_check_all_checkboxes(self, checkboxes_page: CheckboxesPage):
        """Both checkboxes should be checkable."""
        checkboxes_page.navigate()
        checkboxes_page.check_checkbox1()
        checkboxes_page.check_checkbox2()
        assert checkboxes_page.is_checkbox1_checked()
        assert checkboxes_page.is_checkbox2_checked()

    def test_uncheck_all_checkboxes(self, checkboxes_page: CheckboxesPage):
        """Both checkboxes should be uncheckable."""
        checkboxes_page.navigate()
        checkboxes_page.uncheck_checkbox1()
        checkboxes_page.uncheck_checkbox2()
        assert not checkboxes_page.is_checkbox1_checked()
        assert not checkboxes_page.is_checkbox2_checked()

    @pytest.mark.parametrize(
        "checkbox_num,action,expected",
        [
            (1, "check", True),
            (1, "uncheck", False),
            (2, "check", True),
            (2, "uncheck", False),
        ],
        ids=["check_cb1", "uncheck_cb1", "check_cb2", "uncheck_cb2"],
    )
    def test_checkbox_actions_parametrized(
        self, checkboxes_page: CheckboxesPage, checkbox_num: int, action: str, expected: bool
    ):
        """Parametrized checkbox actions test.
        
        Args:
            checkboxes_page: CheckboxesPage fixture
            checkbox_num: Checkbox number (1 or 2)
            action: Action to perform (check or uncheck)
            expected: Expected state after action
        """
        checkboxes_page.navigate()

        if checkbox_num == 1:
            if action == "check":
                checkboxes_page.check_checkbox1()
            else:
                checkboxes_page.uncheck_checkbox1()
            assert checkboxes_page.is_checkbox1_checked() == expected
        else:
            if action == "check":
                checkboxes_page.check_checkbox2()
            else:
                checkboxes_page.uncheck_checkbox2()
            assert checkboxes_page.is_checkbox2_checked() == expected
