"""
Category api
"""

from core_visualization_app.settings import CQL_NAMESPACE
from core_visualization_app.components.category.models import Category
from core_visualization_app.components.category import operations

import core_explore_tree_app.parser.parser as ontology_parser


def get_all_categories_names():
    """Return the list of all the categories names

    Returns:

    """
    return Category.get_all_categories_names()


def toggle_category_selection(category_name):
    """Toggle the boolean that indicates if a category is selected or not.
    Return the category with the given category name

    Args:
        category_name:

    Returns:

    """
    return Category.toggle_category_selection(category_name)


def get_subcategories(category):
    """Return the subcategories list belonging to the given category

    Args:
        category:

    Returns:

    """
    return Category.get_subcategories(category)


def get_subcategories_tuples(categories, categories_tree):
    """Get all the existing categories subclasses (ie. subcategories) from the active ontology as a list of tuples

    Args:
        categories: (Build and powder only for now)
        categories_tree:  ordereddict of each category)

    Returns: List of list of tuples. Each tuple is a subclass of a category (ie. a subcategory) and a list gathers all
    the subclasses of a single category. There are as many lists as categories

    """
    subcategories_tuples_list = operations.get_subcategories_tuples(
        categories, categories_tree
    )

    return subcategories_tuples_list


def get_categories(active_ontology):
    """Return category tuples, a list of tuples. Each tuple is a category.
     Return also categories tree, a list of dict. Each dict contains the ontology annotation part related
     to the category which is at the same index within the category tuples.

    Args:
        active_ontology:

    Returns:

    """
    tree = ontology_parser.parse_ontology(active_ontology.content)
    owl_node_categories = CQL_NAMESPACE + "AMTests"
    categories_tree = []
    categories_tuples = []

    for ontology_key, ontology_value in list(tree.items()):
        if ontology_key != owl_node_categories:
            continue
        for sub_dict_key, sub_dict_value in list(ontology_value.items()):
            if sub_dict_key == "children":
                for category_path, category_tree in list(sub_dict_value.items()):
                    category = category_path.split(CQL_NAMESPACE)[1]
                    Category.create_category(category)
                    categories_tuples.append((category, category))
                    categories_tree.append(category_tree)

    return categories_tuples, categories_tree


def get_category_by_name(category_name):
    """Return the category object with the given argument

    Args:
        category_name:

    Returns:

    """
    return Category.get_category_by_name(category_name)


def get_selected_category_name():
    """Return the only one selected category object name

    Returns:

    """
    return Category.get_selected_category_name()


def delete_all_categories():
    """Delete all the Category objects

    Returns:

    """
    return Category.delete_all_categories()
