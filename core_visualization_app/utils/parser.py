import unicodedata


def parse_cell(value):
    """Return the parsed value to insert it within the data table.

    Args:
        value:

    Returns:

    """
    if value:
        dict_value = str(value)
    else:
        dict_value = ""

    value = ""
    dict_value.split(",")

    for elt in dict_value:
        if not elt == ",":
            value += elt

    return value
