import pytest
from pages.drag_drop_page import DragDropPage


@pytest.mark.regression
@pytest.mark.drag_drop
class TestDragDrop:
    """Test suite for drag and drop functionality."""

    def test_page_loads(self, drag_drop_page: DragDropPage):
        """Drag and drop page should load."""
        drag_drop_page.navigate()
        assert "The Internet" in drag_drop_page.get_title()

    def test_initial_column_a_text(self, drag_drop_page: DragDropPage):
        """Column A should contain 'A' initially."""
        drag_drop_page.navigate()
        assert "A" in drag_drop_page.get_column_a_text()

    def test_initial_column_b_text(self, drag_drop_page: DragDropPage):
        """Column B should contain 'B' initially."""
        drag_drop_page.navigate()
        assert "B" in drag_drop_page.get_column_b_text()

    def test_drag_a_to_b_swaps_columns(self, drag_drop_page: DragDropPage):
        """Dragging A to B should swap column contents."""
        drag_drop_page.navigate()
        drag_drop_page.drag_a_to_b()
        # After drag: column A position should have B, column B position should have A
        assert "B" in drag_drop_page.get_column_a_text()
        assert "A" in drag_drop_page.get_column_b_text()

    def test_drag_b_to_a_swaps_back(self, drag_drop_page: DragDropPage):
        """Dragging B back to A should restore original order."""
        drag_drop_page.navigate()
        drag_drop_page.drag_a_to_b()
        drag_drop_page.drag_b_to_a()
        assert "A" in drag_drop_page.get_column_a_text()
        assert "B" in drag_drop_page.get_column_b_text()

    def test_multiple_sequential_drags(self, drag_drop_page: DragDropPage):
        """Multiple sequential drag operations should work correctly."""
        drag_drop_page.navigate()
        
        # Initial state
        assert "A" in drag_drop_page.get_column_a_text()
        
        # First drag
        drag_drop_page.drag_a_to_b()
        assert "B" in drag_drop_page.get_column_a_text()
        
        # Second drag to swap back
        drag_drop_page.drag_b_to_a()
        assert "A" in drag_drop_page.get_column_a_text()
