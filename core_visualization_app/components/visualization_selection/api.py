"""
Visualization Selection api
"""

from core_visualization_app.components.visualization_selection.models import Category, Projects, SelectedTest


def get_all_categories_names():
    """ Return the list of all the categories names

    Returns:

    """
    return Category.get_all_categories_names()


def get_projects(navigation, template_id):
    """ Get all the existing projects from the database

    :param navigation:
    :param template_id:
    :return: list of tuples. Each tuple is a project written twice to be consistent with form syntax
    """
    return Projects.get_projects(navigation, template_id)


def create_project(project_name):
    """ Create project with the given argument as project name and return the project

    Args:
        project_name:

    Returns:

    """
    return Projects.create_project(project_name)


def get_all_projects_list(navigation, template_id):
    """ Return the list of the projects names tuples to put in the Django forms

    Args:
        navigation:
        template_id:

    Returns:

    """
    return Projects.get_all_projects_list(navigation, template_id)


def get_project_by_name(project_name):
    """ Return the project with the given name

    Args:
        project_name:

    Returns:

    """
    return Projects.get_project_by_name(project_name)


def toggle_project_selection(project_name, selection):
    """ Toggle the boolean that indicates if a project is selected or not.
    Return the project with the given project name

    Args:
        project_name:
        selection:

    Returns:

    """
    return Projects.toggle_project_selection(project_name, selection)


def get_selected_projects_name():
    """ Return the list of all the projects names whose 'is_selected' is True

    Returns:

    """
    return Projects.get_selected_projects_name()


def toggle_category_selection(category_name):
    """ Toggle the boolean that indicates if a category is selected or not.
    Return the category with the given category name

    Args:
        category_name:

    Returns:

    """
    return Category.toggle_category_selection(category_name)


def get_subcategories(category):
    """ Return the subcategories list belonging to the given category

    Args:
        category:

    Returns:

    """
    return Category.get_subcategories(category)


def get_subcategories_tuples(categories, categories_tree):
    """ Get all the existing categories subclasses (ie. subcategories) from the active ontology as a list of tuples

    :param categories (Build and powder only for now)
    :param categories_tree (ordereddict of each category)
    :return: list of list of tuples. Each tuple is a subclass of a category (ie. a subcategory) and a list gathers all
    the subclasses of a single category. There are as many lists as categories
    """
    return Category.get_subcategories_tuples(categories, categories_tree)


def get_categories(active_ontology):
    """ Return category tuples, a list of tuples. Each tuple is a category.
     Return also categories tree, a list of dict. Each dict contains the ontology annotation part related
     to the category which is at the same index within the category tuples.

    :param active_ontology:
    :return:
    """
    return Category.get_categories(active_ontology)


def get_category_by_name(category_name):
    """ Return the category object with the given argument

    Args:
        category_name:

    Returns:

    """
    return Category.get_category_by_name(category_name)


def get_selected_category_name():
    """ Return the only one selected category object name

    Returns:

    """
    return Category.get_selected_category_name()


def create_selected(selected_name):
    """ Create and return a selected test

    Args:
        selected_name:

    Returns:

    """
    return SelectedTest.create_selected(selected_name)


def toggle_test_selection(selected_test_name):
    """ Toogle the test selection. Only one test can be selected at the same time, all the other selected test are
    updated as 'is selected' = False while the one corresponding
    to the given test name 'is selected' field is updated as True.

    Args:
        selected_test_name:

    Returns:

    """
    return SelectedTest.toggle_test_selection(selected_test_name)


def get_selected_test():
    """ Return the selected test whose 'is selected' field is True

    Returns:

    """
    return SelectedTest.get_selected_test()


def delete_all_projects():
    """ Delete all projects

    Returns:

    """
    return Projects.delete_all_projects()
