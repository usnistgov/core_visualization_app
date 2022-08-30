"""Visualization  parser utils operations"""

from core_visualization_app.settings import CQL_NAMESPACE
import core_explore_tree_app.components.data.query as query_database_api
from core_visualization_app.utils import dict as dict_utils


def get_all_projects_list(navigation, template_id):
    """Return the list of the projects names tuples to put in the Django forms

    Args:
        navigation:
        template_id:

    Returns:

    """
    projects_id_tuples = get_projects(navigation, template_id)
    all_projects_list = []
    for project_tuple in projects_id_tuples:
        all_projects_list.append(project_tuple[0])
    return all_projects_list


def get_projects(navigation, template_id):
    """Get all the existing projects from the database

    Args:
        navigation:
        template_id:

    Returns: list of tuples. Each tuple is a project written twice to be consistent with form syntax

    """
    # Get the filter related to the projects
    owl_node_project = CQL_NAMESPACE + "AMProject"
    navigation_projects = navigation.get_by_name(owl_node_project)

    projects_id = []

    # All the navigation objects are identical so it is enough to get the information we need from the first one
    if (
        "filter" in navigation_projects[0].options
        and navigation_projects[0].options["filter"] is not None
    ):
        project_filter = navigation_projects[0].options["filter"]
    if (
        "projection" in navigation_projects[0].options
        and navigation_projects[0].options["projection"] is not None
    ):
        project_projection = navigation_projects[0].options["projection"]

    if not (project_filter and project_projection is None):
        projects = query_database_api.execute_query(
            template_id, [project_filter], project_projection
        )
        for project in projects:
            project_id = dict_utils.get_dict_value(project.dict_content, "projectID")
            if project_id not in projects_id:
                projects_id.append(project_id)

    projects_id_tuples = []
    for project_id in projects_id:
        projects_id_tuples.append((project_id, project_id))

    return projects_id_tuples
