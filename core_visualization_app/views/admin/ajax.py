import json

from django.core.cache import caches
from django.http import HttpResponse, HttpResponseBadRequest

import core_explore_tree_app.components.query_ontology.api as query_ontology_api
import core_explore_tree_app.parser.parser as ontology_parser
import core_visualization_app.components.visualization_data.api as visualization_data_api
import core_visualization_app.components.visualization_data.operations as visualization_data_operations
import core_visualization_app.components.visualization_selection.api as visualization_selection_api
from core_explore_tree_app.components.navigation.api import create_navigation_tree_from_owl_file
from core_visualization_app.utils import dict as visualization_utils

navigation_cache = caches['navigation']

CQL_NAMESPACE = "http://siam.nist.gov/Database-Navigation-Ontology#"


def build_visualization_data(request):
    """ Build data table object

    :param request:
    :return:
    """
    try:
        # get the active ontology
        active_ontology = query_ontology_api.get_active()
        template_id = active_ontology.template.id
        nav_key = active_ontology.id

        # get the navigation from the cache
        if nav_key in navigation_cache:  # if template_id in navigation_cache:
            navigation = navigation_cache.get(nav_key)  # navigation_cache.get(template_id)
        else:
            # create the navigation
            navigation = create_navigation_tree_from_owl_file(active_ontology.content)
            navigation_cache.set(nav_key, navigation)  # navigation_cache.set(template_id, navigation)

        # Reset the projects
        visualization_selection_api.delete_all_projects()

        # Get the existing projects from the navigation
        all_projects_list = visualization_selection_api.get_all_projects_list(navigation, template_id)

        # Get the AM Tests branch from the all ontology tree
        all_tree = ontology_parser.parse_ontology(active_ontology.content)
        owl_main_node = CQL_NAMESPACE + 'AMTests'
        am_tests_tree = all_tree[owl_main_node]

        # List of dicts. Each dict is a AM Test subcategory data_table visualization annotation
        data_table_annotations = []

        category_trees = visualization_utils.get_children_trees(am_tests_tree)

        # Load all the test types trees within the data table annotations list
        for category_tree in category_trees:
            test_type_trees = visualization_utils.get_children_trees(category_tree.values()[0])
            for test_type_tree in test_type_trees:
                check_tree = visualization_utils.check_children(test_type_tree)
                for tree in check_tree:
                    data_table_annotations.append(tree)

        # Each dict is like {test_name: visualization_annotation_dict}
        for test_type_tree in data_table_annotations:
            loc = data_table_annotations.index(test_type_tree)
            data_table_annotations[loc] = {test_type_tree.keys()[0]: json.loads(test_type_tree.values()[0]['annotations']['visualization'])}

        # Delete all old data line objects
        visualization_data_api.delete_all()

        # Create all DataLine objects
        for data_table_annotation in data_table_annotations:
            visualization_data_operations.load_test_data(data_table_annotation, all_projects_list, template_id)

        return HttpResponse(json.dumps({}), content_type='application/javascript')

    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')




