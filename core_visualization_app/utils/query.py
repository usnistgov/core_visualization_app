import json

from core_main_app.components.data.models import Data
from core_main_app.system import api as system_api
from core_visualization_app.utils import dict as dict_utils


def execute_query(template_id, filters, projection, path):
    """ Return a list of dict.
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
    #List to return at the end
    data_list_parsed = []

    # Get all data from the given template
    data_id_list = {data.id for data in system_api.get_all_by_list_template([template_id])}

    # Parsing filters if present
    for _filter in filters:
        try:
            # Loads filter and projection
            json_filter = json.loads(_filter)
            json_projection = json.loads(projection)
        except Exception, e:
            print e.message

        filter_result = Data.execute_query(json_filter)

        filter_id = {document.id for document in filter_result}
        if filter_id:

            data_id_list = data_id_list.intersection(filter_id)

            data_list_result = [doc for doc in filter_result if doc.id in data_id_list]

            # Parse the results of the query
            if data_list_result is not None:
                list_of_dicts = dict_utils.get_list_inside_dict(path, data_list_result[0].dict_content)
                temp_dict = {}

                if list_of_dicts:
                    for i in range(0, len(list_of_dicts)):
                        temp_dict.clear()
                        for proj in json_projection: #keys
                            if proj.split('.')[-1] in list_of_dicts[i]:
                                temp_dict[proj.split('.')[-1]] = list_of_dicts[i][proj.split('.')[-1]]
                            if proj.split('.')[-2] in list_of_dicts[i]:  # Specimen build location XYZ is a subdict
                                if isinstance(list_of_dicts[i][proj.split('.')[-2]], dict):
                                    if proj.split('.')[-1] in list_of_dicts[i][proj.split('.')[-2]]:
                                        temp_dict[proj.split('.')[-1]] = list_of_dicts[i][proj.split('.')[-2]][proj.split('.')[-1]]
                        data_list_parsed.append(json.dumps(temp_dict))

                else:
                    data_list_parsed = None

    return data_list_parsed
