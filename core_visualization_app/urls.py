""" Url router for the schema viewer application
"""
from django.urls import re_path

import core_visualization_app.views.user.ajax as user_ajax
import core_visualization_app.views.user.views as user_views

urlpatterns = [
    re_path(r"^$", user_views.index, name="core_visualization_index"),
    re_path(
        r"^select-projects-form",
        user_ajax.get_selected_project,
        name="core_visualization_selected_projects",
    ),
    re_path(
        r"^select-category-form",
        user_ajax.update_selected_category,
        name="core_visualization_selected_category",
    ),
    re_path(
        r"^select-subcategory-form",
        user_ajax.update_selected_subcategory,
        name="core_visualization_selected_subcategory",
    ),
    re_path(
        r"^load-test-data",
        user_ajax.load_test_data,
        name="core_visualization_load_test_data",
    ),
    re_path(
        r"^download-test-data",
        user_ajax.download_test_data,
        name="core_visualization_download_test_data",
    ),
    re_path(
        r"^update-configuration",
        user_ajax.update_configuration,
        name="core_visualization_update_configuration",
    ),
    re_path(
        r"^update-selection-forms",
        user_ajax.update_selection_forms,
        name="core_visualization_update_selection_forms",
    ),
    re_path(
        r"^update-custom-form",
        user_ajax.update_custom_form,
        name="core_visualization_update_custom_form",
    ),
]
