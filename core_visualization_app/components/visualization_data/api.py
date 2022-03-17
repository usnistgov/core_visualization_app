"""
Visualization data api
"""

from core_visualization_app.components.visualization_data.models import DataLine


def create_line(test_type, project_id, doc_id):
    """If DataLine already exists we get it, otherwise it is created and saved.
    Returns the DataLine

    Args:
        test_type:
        project_id:
        doc_id:

    Returns:

    """
    return DataLine.create_line(test_type, project_id, doc_id)


def update_line(test_type, project_id, doc_id, param, value):
    """Update a DataLine and return the updated DataLine

    Args:
        test_type:
        project_id:
        doc_id:
        param:
        value:

    Returns:

    """
    return DataLine.update_line(test_type, project_id, doc_id, param, value)


def is_line(doc_id):
    """Return True if a DataLine exists that gets the given argument as doc_id

    Args:
        doc_id:

    Returns:

    """
    return DataLine.is_line(doc_id)


def get_lines(test_type, projects_list):
    """Return the list of all the DataLine data related to a test type and a projects list

    Args:
        test_type:
        projects_list:

    Returns:

    """
    return DataLine.get_lines(test_type, projects_list)


def delete_all():
    """Delete all the DataLine objects

    Returns:

    """
    return DataLine.delete_all()
