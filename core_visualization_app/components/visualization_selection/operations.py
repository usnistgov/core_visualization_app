"""
Operations on visualization_selection objects
"""

import core_explore_tree_app.components.query_ontology.api as query_ontology_api
import core_explore_tree_app.parser.parser as ontology_parser

CQL_NAMESPACE = "http://siam.nist.gov/Database-Navigation-Ontology#"


def get_category_tree(category_name):
    """ Get the parsed ontology tree related to the given category name

    :param category_name
    :return: category tree
    """
    # get the active ontology
    active_ontology = query_ontology_api.get_active()

    tree = ontology_parser.parse_ontology(active_ontology.content)
    owl_main_node = CQL_NAMESPACE + 'AMTests'
    owl_node_categories = CQL_NAMESPACE + category_name
    categories_tree = 0

    for k, v in tree.items():
        if k == owl_main_node:
            for k2, v2 in v.items():
                if k2 == 'children':
                    for k3, v3 in v2.items():
                        if k3 == owl_node_categories:
                            categories_tree = v3
    return categories_tree


def get_subcategories_list(category_tree):
    """ Get all the category tree subclasses (ie. subcategories)

    :param category_tree related to a single category
    :return: list of subcategories names
    """

    subcategories_list = []
    for k, v in category_tree.items():
        if k == 'children':
            for k2, v2 in v.items():
                if k2.startswith(CQL_NAMESPACE):
                    subcategory = k2.split(CQL_NAMESPACE)[1]
                    subcategories_list.append(subcategory)
                bool = False
                for k3, v3 in v2.items():
                    if k3 == 'children':
                        for k4, v4 in v3.items():
                            if k4.startswith(CQL_NAMESPACE) and not bool:
                                bool = True
                                subcategories_list.remove(subcategory)
                            if k4.startswith(CQL_NAMESPACE):
                                subcategory = k4.split(CQL_NAMESPACE)[1]
                                subcategories_list.append(subcategory)
    return subcategories_list


def get_subcategory_tree(test_selected_name, category_tree):
    """ Get the parsed ontology tree related to the given test selected name

    :param test_selected_name
    :param  category_tree
    :return test selected tree
    """
    owl_node_categories = CQL_NAMESPACE + test_selected_name
    subcategory_tree = 0

    for k, v in category_tree.items():
        if k == 'children':
            for k2, v2 in v.items():
                if k2 == owl_node_categories:
                    subcategory_tree = v2

    return subcategory_tree
