import json

from core_visualization_app.settings import CQL_NAMESPACE


def get_dict_value(dict_content, key):
    """Recursive method to get the value deep inside json tree

    Args:
        dict_content:  json tree
        key:  key related to the value

    Returns:

    """
    value = 0
    for k, v in list(dict_content.items()):
        if k != key:
            return get_dict_value(v, key)
        else:
            value = v
    return value


def get_dict_path_value(dict_content, path):
    """Recursive method to get the value inside json tree from a full path

    Args:
        dict_content:
        path:

    Returns:

    """
    path_list = path.split(".")
    if dict_content:
        try:
            if path_list[0] == "dict_content":
                return get_dict_path_value(
                    dict_content, path[(len(path_list[0]) + 1) :]
                )

            if len(path_list) == 1:

                return dict_content[path]
            else:
                substr_length = len(path_list[0]) + 1  # +1 to substring the point
                return get_dict_path_value(
                    dict_content[path_list[0]], path[substr_length:]
                )
        except:
            return ""
    return ""


def get_test_type_tree(category_tree, test_type_name):
    """Recursive method to get the test selected tree inside a category tree

    Args:
        category_tree: category tree
        test_type_name: test type name

    Returns: test type tree

    """
    owl_node_categories = CQL_NAMESPACE + test_type_name

    if owl_node_categories in list(category_tree.keys()):
        return category_tree[owl_node_categories]

    else:
        if "children" in list(category_tree.keys()):
            return get_test_type_tree(category_tree["children"], test_type_name)
        else:
            item = category_tree.popitem()
            if item[0].startswith(CQL_NAMESPACE):
                return get_test_type_tree(item[1], test_type_name)

    return get_test_type_tree(category_tree, test_type_name)


def get_list_inside_dict(dict_path, dict_content):
    """return a list of a single dict.
    This method goes throughout the dict 'dict_content' given in argument according to the path 'dict_path'

    Args:
        dict_path: key1.key2.key3...keyx
        dict_content: {key1: {key2: {key3:...{keyx:{dict_content_to_return}}

    Returns:

    """
    if not isinstance(dict_path, list):
        dict_path = dict_path.split(".")

    if dict_path[0] == "dict_content":
        dict_path.pop(0)

    if isinstance(dict_content, dict):
        if dict_path[-1] not in json.dumps(dict_content):
            return None
        if len(dict_path) == 1:
            return [dict_content]
        else:
            return get_list_inside_dict(dict_path[1:], dict_content[dict_path[0]])
    else:
        if len(dict_path) != 1:
            return get_dicts_inside_list_of_dict(dict_path, dict_content)
        return dict_content


def get_dicts_inside_list_of_dict(list_path, list_of_dict):
    """

    Args:
        list_path:  [a,b,c]
        list_of_dict:  [{a:{b:{c:value1},{a:{b:{c:value2}, ..]

    Returns: [{c:value1}, {c:value2},..]

    """
    while len(list_path) > 1:
        for dict_to_parse in list_of_dict:
            list_of_dict[list_of_dict.index(dict_to_parse)] = dict_to_parse[
                list_path[0]
            ]
        list_path = list_path[1:]

    if len(list_path) == 1:
        return list_of_dict


def get_children_trees(tree):
    """

    Args:
        tree:  Parent tree

    Returns: List of children trees

    """
    keys_list = []
    for key in list(tree.keys()):
        if key.startswith(CQL_NAMESPACE):
            keys_list.append(key)

    if not keys_list:
        return get_children_trees(tree["children"])

    trees_list = []
    for key in keys_list:
        trees_list.append({key.split("#")[-1]: tree[key]})

    return trees_list


def check_children(tree):
    """

    Args:
        tree: tree to check

    Returns:  list of children trees if the original tree is a Parent. Otherwise return the original tree in a list of 1 elt

    """
    new_tree = list(tree.values())[0]
    if "children" in list(new_tree.keys()):
        if new_tree["children"]:
            check_list = get_children_trees(new_tree)
        else:
            check_list = [tree]
    else:
        check_list = [tree]

    return check_list
