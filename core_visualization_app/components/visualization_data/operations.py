"""
Operations on visualization_data objects
"""
import core_explore_tree_app.components.data.query as query_database_api
import core_visualization_app.components.visualization_data.api as visualization_data_api
from core_visualization_app.utils import dict as visualization_utils
from core_visualization_app.utils import parser as utils_parser

import logging
import json

from core_main_app.system import api as system_api
from core_main_app.components.data.models import Data
from core_visualization_app.utils import dict as dict_utils

logger = logging.getLogger(__name__)


def load_test_data(data_table_annotation, all_projects_list, template_id):
    """Load all visualization test data by querying the database and creates Python objects (DataLine)
    by using the ontology annotation cql:visualization that contains all the queries and path. Syntax of the annotation
    is correlated with this method.

    Args:
        data_table_annotation: Dict corresponding to the ontology visualization tree of a single test type
        all_projects_list: list of all the existing projects of the database
        template_id: template_id

    Returns:

    """
    # There is only one couple key/value in the initial dict.
    # The value content is a list. Only the first element is needed to load the data.
    # This comes from the ontology so it cannot be empty
    test_type = list(data_table_annotation.keys())[0]
    visualization_annotation = list(data_table_annotation.values())[0][0]

    # (list of dicts, 1 dict = 1 parameter)
    data = visualization_annotation["data"]

    # Load the project query path
    project_filter_path = visualization_annotation["project"]

    # Load the test_type filter
    test_type_filter = visualization_annotation["test_type_query"]

    for project in all_projects_list:
        # Load the project filter
        project_filter = {project_filter_path: project}

        # Load query_filter as a list of filters
        query_filter = [json.dumps(project_filter), json.dumps(test_type_filter)]

        # One query for each parameter of the template to get all the data from all the documents
        # related to this single parameter. One query gets 1 projection (only for 'simple data')
        for parameter in data:
            projection = {}

            # SIMPLE DATA
            if "path" in parameter:
                query_path_data(
                    projection, parameter, template_id, query_filter, test_type, project
                )

            # ARRAY DATA
            if "filter" in parameter:
                query_filter_data(
                    parameter, projection, template_id, query_filter, test_type, project
                )

    return None


def update_visualization_data(result_id, test_type, project, parameter_name, value):
    """Check if the data doesn't already exist and create python object DataLine to store
    the visualization data that will be used to plot

    Args:
        result_id:
        test_type:
        project:
        parameter_name:
        value:

    Returns:

    """
    if not visualization_data_api.is_line(result_id):
        visualization_data_api.create_line(test_type, project, result_id)
    visualization_data_api.update_line(
        test_type, project, result_id, parameter_name, value
    )


def query_path_data(
    projection, parameter, template_id, query_filter, test_type, project
):
    """Query and load the visualization data which 'path' is the key within the Ontology annotation 'cql:visualization'

    Args:
        projection:
        parameter:
        template_id:
        query_filter:
        test_type:
        project:

    Returns:

    """
    projection[parameter["path"]] = "1"
    parameter_results = query_database_api.execute_query(
        template_id, query_filter, json.dumps(projection)
    )

    for result in parameter_results:
        parameter_name = parameter["parameter_name"]
        dict_value = visualization_utils.get_dict_path_value(
            result.dict_content, parameter["path"]
        )
        dict_value = utils_parser.parse_cell(dict_value)
        update_visualization_data(
            result.id, test_type, project, parameter_name, dict_value
        )
        # DOUBLE LOOP : One additional query for each result
        if "link_parameters" in parameter:
            for link_parameter in parameter["link_parameters"]:
                parameter_name = link_parameter["parameter_name"]

                query = {link_parameter["link_query"]: dict_value}
                projection.clear()

                parameter_path = link_parameter["path"]
                projection[parameter_path] = "1"
                link_filter = [json.dumps(query)]

                value = get_check_path_value(
                    link_parameter,
                    projection,
                    template_id,
                    link_filter,
                    parameter_path,
                    dict_value,
                )

                dict_link_value = get_dict_link_value(
                    link_parameter, value, query, projection, template_id
                )
                dict_link_value = utils_parser.parse_cell(dict_link_value)
                update_visualization_data(
                    result.id, test_type, project, parameter_name, dict_link_value
                )
    return None


def get_check_path_value(
    link_parameter, projection, template_id, link_filter, parameter_path, dict_value
):
    """In some special cases defined within the ontology annotation 'cql:visualization', we need to check th path of the data query because within the schema,
    different kinds of data may be at the same depth.

    Args:
        link_parameter:
        projection:
        template_id:
        link_filter:
        parameter_path:
        dict_value:

    Returns:

    """
    if "check_path" in link_parameter:
        value = None
        projection[link_parameter["link_query"]] = "1"
        link_value = execute_link_query(
            template_id, link_filter, json.dumps(projection), parameter_path
        )
        for elt in link_value:
            elt = json.loads(elt)
            if link_parameter["link_query"].split(".")[-1] in elt:
                if elt[link_parameter["link_query"].split(".")[-1]] == dict_value:
                    for k, v in list(elt.items()):
                        if k == link_parameter["path"].split(".")[-1]:
                            value = v
    else:
        link_value = query_database_api.execute_query(
            template_id, link_filter, json.dumps(projection)
        )
        if link_value:
            link_value = link_value[0].dict_content
        else:
            link_value = None

        value = visualization_utils.get_dict_path_value(link_value, parameter_path)

    return value


def query_filter_data(
    parameter, projection, template_id, query_filter, test_type, project
):
    """Query and load the visualization data which 'filter' is the key within the Ontology annotation 'cql:visualization'

    Args:
        parameter:
        projection:
        template_id:
        query_filter:
        test_type:
        project:

    Returns:

    """
    if parameter["filter"][0]["type"] == "array":
        projection[parameter["filter"][0]["path"]] = "1"
        parameter_results = query_database_api.execute_query(
            template_id, query_filter, json.dumps(projection)
        )

        for result in parameter_results:
            parsed_result = visualization_utils.get_dict_path_value(
                result.dict_content, parameter["filter"][0]["path"]
            )

            if not isinstance(parsed_result, list):
                parsed_result = [parsed_result]

            for elt in parsed_result:
                parameter_name = ""
                for item in parameter["filter"][0]["items"]:
                    if "parameter_name" in item:
                        name = str(
                            visualization_utils.get_dict_path_value(elt, item["path"])
                        )

                        if parameter_name:
                            parameter_name = parameter_name + " " + name
                        else:
                            parameter_name = name

                    if "parameter_value" in item:
                        dict_value = visualization_utils.get_dict_path_value(
                            elt, item["path"]
                        )
                        dict_value = utils_parser.parse_cell(dict_value)
                        update_visualization_data(
                            result.id, test_type, project, parameter_name, dict_value
                        )
    return None


def get_dict_link_value(link_parameter, value, query, projection, template_id):
    """In some special cases we need to get a data which belongs to another subtree of the ontology. so we need to link
    the data from the other tree to a common a data in the tree the visualization annotation is so we can append the queried
    data to the right group of data.

    Args:
        link_parameter:
        value:
        query:
        projection:
        template_id:

    Returns:

    """
    if "sub_query" in link_parameter:
        if value:
            query.clear()
            query[link_parameter["sub_query"]["query_path"]] = value

            projection.clear()
            parameter_path = link_parameter["sub_query"]["path"]
            projection[parameter_path] = "1"

            link_filter = [json.dumps(query)]

            if "check_path" in link_parameter:
                dict_link_value = None
                projection[link_parameter["sub_query"]["query_path"]] = "1"
                link_value = execute_link_query(
                    template_id, link_filter, json.dumps(projection), parameter_path
                )
                if link_value:
                    for elt in link_value:
                        elt = json.loads(elt)
                        if (
                            link_parameter["sub_query"]["query_path"].split(".")[-1]
                            in elt
                        ):
                            if (
                                elt[
                                    link_parameter["sub_query"]["query_path"].split(
                                        "."
                                    )[-1]
                                ]
                                == value
                            ):
                                for k, v in list(elt.items()):
                                    if k == parameter_path.split(".")[-1]:
                                        dict_link_value = v
                else:
                    dict_link_value = None
            else:
                link_value = query_database_api.execute_query(
                    template_id, link_filter, json.dumps(projection)
                )
                if link_value:
                    link_value = link_value[0].dict_content
                else:
                    link_value = None
                dict_link_value = visualization_utils.get_dict_path_value(
                    link_value, parameter_path
                )
        else:
            dict_link_value = ""

    else:
        dict_link_value = value

    return dict_link_value


def get_data_content(test_name, selected_projects_name):
    """

    Args:
        test_name:  Selected AM Test subcategory
        selected_projects_name:

    Returns: csv_table as a list which is then embeded within the HTML

    """
    parameters_list = []

    for data_line_dict in visualization_data_api.get_lines(
        test_name, selected_projects_name
    ):
        for param in list(data_line_dict.keys()):
            if param not in parameters_list:
                parameters_list.append(param)

    data_table_list = [parameters_list]
    for data_line_dict in visualization_data_api.get_lines(
        test_name, selected_projects_name
    ):
        row = [""] * len(parameters_list)
        for param in parameters_list:
            if param in list(data_line_dict.keys()):
                row[parameters_list.index(param)] = data_line_dict[param]
        data_table_list.append(row)

    # Delete empty columns
    data_table_list = list(zip(*data_table_list))
    data_table_list = [x for x in data_table_list if any(x[1:])]
    data_table_list = [list(row) for row in zip(*data_table_list)]

    return data_table_list


def execute_link_query(template_id, filters, projection, path):
    """Return a list of dict.
    Execute queries with a path that do not belong to the visualization annotation ontology.
    So this method is used to get a 'link value' which is both in the visualization annotation and the another
    ontology annotation. The link value allows to identify the value from the other ontology annotation
    to the visualization right DataLine.

    Args:
        template_id:
        filters:
        projection:
        path:

    Returns:

    """
    # List to return at the end
    data_list_parsed = []

    # Get all data from the given template
    data_id_list = {
        data.id for data in system_api.get_all_by_list_template([template_id])
    }

    # Parsing filters if present
    for _filter in filters:
        try:
            # Loads filter and projection
            json_filter = json.loads(_filter)
            json_projection = json.loads(projection)
        except Exception as e:
            logger.error(str(e))

        filter_result = Data.execute_query(json_filter, [])

        filter_id = {document.id for document in filter_result}
        if filter_id:

            data_id_list = data_id_list.intersection(filter_id)

            data_list_result = [doc for doc in filter_result if doc.id in data_id_list]

            # Parse the results of the query
            if data_list_result is not None:
                list_of_dicts = dict_utils.get_list_inside_dict(
                    path, data_list_result[0].dict_content
                )
                temp_dict = {}

                if list_of_dicts:
                    for i in range(0, len(list_of_dicts)):
                        temp_dict.clear()
                        for proj in json_projection:  # keys
                            if proj.split(".")[-1] in list_of_dicts[i]:
                                temp_dict[proj.split(".")[-1]] = list_of_dicts[i][
                                    proj.split(".")[-1]
                                ]
                            if (
                                proj.split(".")[-2] in list_of_dicts[i]
                            ):  # Specimen build location XYZ is a subdict
                                if isinstance(
                                    list_of_dicts[i][proj.split(".")[-2]], dict
                                ):
                                    if (
                                        proj.split(".")[-1]
                                        in list_of_dicts[i][proj.split(".")[-2]]
                                    ):
                                        temp_dict[proj.split(".")[-1]] = list_of_dicts[
                                            i
                                        ][proj.split(".")[-2]][proj.split(".")[-1]]
                        data_list_parsed.append(json.dumps(temp_dict))

                else:
                    data_list_parsed = None

    return data_list_parsed
