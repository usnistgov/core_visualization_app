"""
Operations on visualization_data objects
"""

import json

import core_explore_tree_app.components.data.query as query_database_api
import core_visualization_app.components.visualization_data.api as visualization_data_api
from core_visualization_app.utils import dict as visualization_utils
from core_visualization_app.utils import parser as utils_parser
from core_visualization_app.utils import query as query_utils


def load_test_data(data_table_annotation, all_projects_list, template_id):
    """ Load all visualization test data by querying the database and creates Python objects (DataLine)
    by using the ontology annotation cql:visualization that contains all the queries and path. Syntax of the annotation
    is correlated with this method.

    :param data_table_annotation: Dict corresponding to the ontology visualization tree of a single test type
    :param all_projects_list: list of all the existing projects of the database
    :param template_id: template_id
    :return:
    """
    # There is only one couple key/value in the initial dict.
    # The value content is a list. Only the first element is needed to load the data.
    # This comes from the ontology so it cannot be empty
    test_type = data_table_annotation.keys()[0]
    visualization_annotation = data_table_annotation.values()[0][0]

    # (list of dicts, 1 dict = 1 parameter)
    data = visualization_annotation['data']

    # Load the project query path
    project_filter_path = visualization_annotation['project']

    # Load the test_type filter
    test_type_filter = visualization_annotation['test_type_query']

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
            if 'path' in parameter:
                projection[parameter['path']] = '1'
                parameter_results = query_database_api.execute_query(template_id, query_filter, json.dumps(projection))

                for result in parameter_results:
                    parameter_name = parameter['parameter_name']
                    dict_value = visualization_utils.get_dict_path_value(result.dict_content, parameter['path'])
                    dict_value = utils_parser.parse_cell(dict_value)
                    if not visualization_data_api.is_line(result.id):
                        visualization_data_api.create_line(test_type,
                                                           project,
                                                           result.id)
                    visualization_data_api.update_line(test_type,
                                                       project,
                                                       result.id,
                                                       parameter_name,
                                                       dict_value)

                    # DOUBLE LOOP : One additional query for each result
                    if 'link_parameters' in parameter:
                        for link_parameter in parameter['link_parameters']:
                            parameter_name = link_parameter['parameter_name']

                            query = {link_parameter['link_query']: dict_value}
                            projection.clear()

                            parameter_path = link_parameter['path']
                            projection[parameter_path] = '1'
                            link_filter = [json.dumps(query)]

                            if 'check_path' in link_parameter:
                                value = None
                                projection[link_parameter['link_query']] = '1'
                                link_value = query_utils.execute_query(template_id,
                                                                       link_filter,
                                                                       json.dumps(projection),
                                                                       parameter_path)
                                for elt in link_value:
                                    elt = json.loads(elt)
                                    if link_parameter['link_query'].split('.')[-1] in elt:
                                        if elt[link_parameter['link_query'].split('.')[-1]] == dict_value:
                                            for k, v in elt.items():
                                                if k == link_parameter['path'].split('.')[-1]:
                                                    value = v
                            else:
                                link_value = query_database_api.execute_query(template_id,
                                                                              link_filter,
                                                                              json.dumps(projection))
                                if link_value:
                                    link_value = link_value[0].dict_content
                                else:
                                    link_value = None
                                value = visualization_utils.get_dict_path_value(link_value,
                                                                                parameter_path)

                            if 'sub_query' in link_parameter:
                                if value:
                                    query.clear()
                                    query[link_parameter['sub_query']['query_path']] = value

                                    projection.clear()
                                    parameter_path = link_parameter['sub_query']['path']
                                    projection[parameter_path] = '1'

                                    link_filter = [json.dumps(query)]

                                    if 'check_path' in link_parameter:
                                        dict_link_value = None
                                        projection[link_parameter['sub_query']['query_path']] = '1'
                                        link_value = query_utils.execute_query(template_id,
                                                                               link_filter,
                                                                               json.dumps(projection),
                                                                               parameter_path)
                                        if link_value:
                                            for elt in link_value:
                                                elt = json.loads(elt)
                                                if link_parameter['sub_query']['query_path'].split('.')[-1] in elt:
                                                    if elt[link_parameter['sub_query']['query_path'].split('.')[-1]] == value:
                                                        for k, v in elt.items():
                                                            if k == parameter_path.split('.')[-1]:
                                                                dict_link_value = v
                                        else:
                                            dict_link_value = None
                                    else:
                                        link_value = query_database_api.execute_query(template_id,
                                                                                      link_filter,
                                                                                      json.dumps(projection))
                                        if link_value:
                                            link_value = link_value[0].dict_content
                                        else:
                                            link_value = None
                                        dict_link_value = visualization_utils.get_dict_path_value(link_value,
                                                                                                  parameter_path)
                                else:
                                    dict_link_value = ''

                            else:
                                dict_link_value = value

                            dict_link_value = utils_parser.parse_cell(dict_link_value)
                            if not visualization_data_api.is_line(result.id):
                                visualization_data_api.create_line(test_type,
                                                                   project,
                                                                   result.id)
                            visualization_data_api.update_line(test_type,
                                                               project,
                                                               result.id,
                                                               parameter_name,
                                                               dict_link_value)

            # array parameter with simple path
            if 'filter' in parameter:
                if parameter['filter'][0]['type'] == 'array':
                    projection[parameter['filter'][0]['path']] = '1'
                    parameter_results = query_database_api.execute_query(template_id, query_filter,
                                                                         json.dumps(projection))

                    for result in parameter_results:
                        parsed_result = visualization_utils.get_dict_path_value(result.dict_content,
                                                                                parameter['filter'][0]['path'])

                        if not isinstance(parsed_result, list):
                            parsed_result = [parsed_result]

                        for elt in parsed_result:
                            parameter_name = ''
                            for item in parameter['filter'][0]['items']:
                                if 'parameter_name' in item:

                                    name = str(visualization_utils.get_dict_path_value(elt, item['path']))

                                    if parameter_name:
                                        parameter_name = parameter_name + ' ' + name
                                    else:
                                        parameter_name = name

                                if 'parameter_value' in item:
                                    dict_value = visualization_utils.get_dict_path_value(elt, item['path'])
                                    dict_value = utils_parser.parse_cell(dict_value)
                                    if not visualization_data_api.is_line(result.id):
                                        visualization_data_api.create_line(test_type, project,
                                                                           result.id)
                                    visualization_data_api.update_line(test_type, project,
                                                                       result.id, parameter_name,
                                                                       dict_value)
    return None


def get_data_content(test_name, selected_projects_name):
    """

    :param test_name: Selected AM Test subcategory
    :param selected_projects_name:
    :return: csv_table which mis then embeded within the HTML
    """
    parameters_list = []

    for data_line_dict in visualization_data_api.get_lines(test_name, selected_projects_name):
        for param in data_line_dict.keys():
            if param not in parameters_list:
                parameters_list.append(param)

    data_table_list = [parameters_list]
    for data_line_dict in visualization_data_api.get_lines(test_name, selected_projects_name):
        row = [''] * len(parameters_list)
        for param in parameters_list:
            if param in data_line_dict.keys():
                row[parameters_list.index(param)] = data_line_dict[param]
        data_table_list.append(row)

    return data_table_list
