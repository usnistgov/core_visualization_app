"""
Operations on category objects
"""

from core_visualization_app.settings import CQL_NAMESPACE
import core_explore_tree_app.components.query_ontology.api as query_ontology_api
import core_explore_tree_app.parser.parser as ontology_parser


def get_category_tree(category_name):
    """Get the parsed ontology tree related to the given category name

    Args:
        category_name:

    Returns:

    """
    # get the active ontology
    active_ontology = query_ontology_api.get_active()

    tree = ontology_parser.parse_ontology(active_ontology.content)
    owl_main_node = CQL_NAMESPACE + "AMTests"
    owl_node_categories = CQL_NAMESPACE + category_name
    categories_tree = 0

    for ontology_key, ontology_value in list(tree.items()):
        if ontology_key != owl_main_node:
            continue
        categories_tree = get_children_child_tree(ontology_value, owl_node_categories)
    return categories_tree


def get_subcategory_tree(test_selected_name, category_tree):
    """Get the parsed ontology tree related to the given test selected name

    Args:
        test_selected_name:
        category_tree:

    Returns:

    """
    owl_node_categories = CQL_NAMESPACE + test_selected_name
    subcategory_tree = get_children_child_tree(category_tree, owl_node_categories)

    return subcategory_tree


def get_children_child_tree(tree, key):
    """Return the value of a dict corresponding to the key given as argument. This dict must be a child of the
    tree given as argument and 'children' is the parent key.

    Args:
        tree:
        key:

    Returns:

    """
    child_tree = None

    for tree_key, tree_value in list(tree.items()):
        if tree_key != "children":
            continue
        for sub_key, sub_tree in list(tree_value.items()):
            if sub_key == key:
                child_tree = sub_tree

    return child_tree


def get_subcategories_list(category_name, category_tree):
    """Get all the category tree subclasses (ie. subcategories)

    :param category_tree related to a single category
    :return: list of subcategories names
    """
    subcategories_tuples = get_subcategories_tuples(category_name, category_tree)
    subcategories_list = []
    for i in range(1, len(subcategories_tuples), 2):
        for subcategory_tuple in subcategories_tuples[i]:
            subcategories_list.append(subcategory_tuple[0])

    return subcategories_list


def get_subcategories_tuples(categories, categories_tree):
    """Get all the existing categories subclasses (ie. subcategories) from the active ontology as a list of tuples

    :param categories (Build and powder only for now)
    :param categories_tree (ordereddict of each category)
    :return: list of list of tuples. Each tuple is a subclass of a category (ie. a subcategory) and a list gathers all
    the subclasses of a single category. There are as many lists as categories
    """
    subcategories_tuples_list = ()
    i = 0
    for category_tree in categories_tree:
        category = categories[i]
        subcategories = []
        i += 1
        for k, v in list(category_tree.items()):
            if k == "children":
                for k2, v2 in list(v.items()):
                    if k2.startswith(CQL_NAMESPACE):
                        subcategory = k2.split(CQL_NAMESPACE)[1]
                        subcategories.append((subcategory, subcategory))
                    bool = False
                    for k3, v3 in list(v2.items()):
                        if k3 == "children":
                            for k4, v4 in list(v3.items()):
                                if k4.startswith(CQL_NAMESPACE) and not bool:
                                    bool = True
                                    subcategories.remove((subcategory, subcategory))
                                if k4.startswith(CQL_NAMESPACE):
                                    subcategory = k4.split(CQL_NAMESPACE)[1]
                                    subcategories.append((subcategory, subcategory))
                subcategories_tuples_list += (category, subcategories)

    return subcategories_tuples_list
