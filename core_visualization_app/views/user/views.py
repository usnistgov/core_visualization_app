""" Visualization app user views
"""
import json

from django.core.cache import caches
from django.http.response import HttpResponse, HttpResponseBadRequest
from rest_framework.status import HTTP_404_NOT_FOUND

import core_explore_tree_app.components.query_ontology.api as query_ontology_api
from core_explore_tree_app.components.navigation.api import create_navigation_tree_from_owl_file
from core_main_app.commons import exceptions
from core_main_app.utils.rendering import render
from core_visualization_app.components.visualization_selection import api
from core_visualization_app.views.user.forms import SelectProjects, SelectTestCategory, SelectTestSubcategory

navigation_cache = caches['navigation']

CQL_NAMESPACE = "http://siam.nist.gov/Database-Navigation-Ontology#"


def index(request):
    """ Visualization app initial homepage

    Args:
        request:

    Returns:

    """
    error = None
    active_ontology = None

    try:
        # Set up the needed explore tree related objects to get the queries
        # get the active ontology
        active_ontology = query_ontology_api.get_active()
    except exceptions.DoesNotExist:
        error = {"error": "An Ontology should be active to explore. Please contact an admin."}

    if error is None:
        try:
            # Get the active ontology's ID
            template_id = active_ontology.template.id
            nav_key = active_ontology.id

            # get the navigation from the cache
            if nav_key in navigation_cache:  # if template_id in navigation_cache:
                navigation = navigation_cache.get(nav_key)  # navigation_cache.get(template_id)
            else:
                # create the navigation
                navigation = create_navigation_tree_from_owl_file(active_ontology.content)
                navigation_cache.set(nav_key, navigation)  # navigation_cache.set(template_id, navigation)

            # Delete all projects from a previous instance
            api.delete_all_projects()

            # Get the existing projects from the navigation
            projects_tuples = api.get_projects(navigation, template_id)
            select_projects = SelectProjects()
            select_projects.fields['projects'].choices = projects_tuples

            # Get the existing categories from the ontology
            categories_tuples, categories_tree = api.get_categories(active_ontology)
            select_category = SelectTestCategory()
            select_category.fields['categories'].choices = categories_tuples

            # Get the existing subcategories from the ontology
            subcategories_tuples_list = api.get_subcategories_tuples(categories_tuples, categories_tree)
            select_subcategory_tuples = []

            for i in range(1, len(subcategories_tuples_list), 2):
                for tuples in subcategories_tuples_list[i]:
                    select_subcategory_tuples.append(tuples)
            select_subcategory = SelectTestSubcategory()
            select_subcategory.fields['subcategories'].choices = select_subcategory_tuples

        except exceptions.DoesNotExist as e_does_not_exist:
            error = {"error": e_does_not_exist.message}
        except Exception as e:
            error = {"error": e.message}

    if error:
        context = error
    else:
        context = {
            'project': select_projects,
            'subcategories': select_subcategory,
            'categories': select_category,
        }

    assets = {
        "js": [
            {
                "path": 'core_visualization_app/user/js/select_projects_form.js',
                "is_raw": False
            },
            {
                "path": 'core_visualization_app/user/js/select_category_form.js',
                "is_raw": False
            },
            {
                "path": 'core_visualization_app/user/js/select_subcategory_form.js',
                "is_raw": False
            },
            {
                "path": 'core_visualization_app/user/js/load_data_table.js',
                "is_raw": False
            },
            {
                "path": 'core_visualization_app/user/js/download_data_table.js',
                "is_raw": False
            },
        ]
    }
    return render(request, "core_visualization_app/user/visualization.html",
                  assets=assets,
                  context=context)

