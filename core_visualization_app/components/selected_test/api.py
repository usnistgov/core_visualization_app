"""
Selected Test api
"""
from core_visualization_app.components.selected_test.models import SelectedTest


def create_selected(selected_name):
    """Create and return a selected test

    Args:
        selected_name:

    Returns:

    """
    return SelectedTest.create_selected(selected_name)


def toggle_test_selection(selected_test_name):
    """Toogle the test selection. Only one test can be selected at the same time, all the other selected test are
    updated as 'is selected' = False while the one corresponding
    to the given test name 'is selected' field is updated as True.

    Args:
        selected_test_name:

    Returns:

    """
    return SelectedTest.toggle_test_selection(selected_test_name)


def get_selected_test():
    """Return the selected test whose 'is selected' field is True

    Returns:

    """
    return SelectedTest.get_selected_test()
