""" Url router for the schema viewer application
"""
from django.conf.urls import url

import core_visualization_app.views.user.ajax as user_ajax
import core_visualization_app.views.user.views as user_views

urlpatterns = [
    url(r'^$', user_views.index,
        name='core_visualization_index'),
    url(r'^select-projects-form', user_ajax.get_selected_project,
        name='core_visualization_selected_projects'),
    url(r'^select-category-form', user_ajax.update_selected_category,
        name='core_visualization_selected_category'),
    url(r'^select-subcategory-form', user_ajax.update_selected_subcategory,
        name='core_visualization_selected_subcategory'),
    url(r'^load-test-data', user_ajax.load_test_data,
        name='core_visualization_load_test_data'),
    url(r'^download-test-data', user_ajax.download_test_data,
        name='core_visualization_download_test_data'),
    url(r'^update-configuration', user_ajax.update_configuration,
        name='core_visualization_update_configuration'),
    url(r'^update-selection-forms', user_ajax.update_selection_forms,
        name='core_visualization_update_selection_forms'),
    url(r'^update-custom-form', user_ajax.update_custom_form,
        name='core_visualization_update_custom_form'),
    ]






