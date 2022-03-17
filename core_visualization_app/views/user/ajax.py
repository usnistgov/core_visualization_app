""" Visualization selection user ajax file
"""

import csv
import json
from os import path, remove

from django.http import HttpResponseBadRequest, HttpResponse
from django.template import loader

from core_main_app.utils.file import get_file_http_response
from core_visualization_app.components.visualization_configuration import (
    api as visualization_configuration_api,
)
from core_visualization_app.components.visualization_configuration import (
    operations as plots_operations,
)
from core_visualization_app.components.visualization_data import (
    operations as visualization_data_operations,
)
from core_visualization_app.components.projects import api as projects_api
from core_visualization_app.components.category import api as category_api
from core_visualization_app.components.selected_test import api as selected_test_api

from core_visualization_app.components.category import operations as category_operations
from core_visualization_app.utils import dict as utils_dict
from core_visualization_app.views.user.forms import (
    SelectXParameter,
    SelectYParameter,
    SelectCustomizedParameter,
)


def get_selected_project(request):
    """Get the selected projects

    Args:
        request:

    Returns:
    """
    try:
        project_name = request.POST.get("project", None)
        project = projects_api.get_project_by_name(project_name)
        projects_api.toggle_project_selection(project.name, project.is_selected)
        return HttpResponse(project.name)
    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type="application/javascript")


def update_selected_category(request):
    """Get the selected category

    Args:
        request:

    Returns:
    """
    try:
        category_name = request.POST.get("category", None)
        category = category_api.toggle_category_selection(category_name)
        subcategories = category_api.get_subcategories(category)
        return HttpResponse(json.dumps(subcategories), "application/javascript")
    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type="application/javascript")


def update_selected_subcategory(request):
    """Update the selected test ie. subcategory


    Args:
        request:

    Returns:
    """
    try:
        selected_name = request.POST.get("subcategory", None)
        selected_test = selected_test_api.create_selected(selected_name)
        selected_test_api.toggle_test_selection(selected_test.name)
        return HttpResponse("application/javascript")
    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type="application/javascript")


def load_test_data(request):
    """load the test data table into the visualization page

    Args:
        request:

    Returns:
    """
    try:
        test_selected = selected_test_api.get_selected_test()
        selected_projects_name = projects_api.get_selected_projects_name()

        category_name = category_api.get_selected_category_name()
        category_tree = category_operations.get_category_tree(category_name)
        test_selected_tree = utils_dict.get_test_type_tree(
            category_tree, test_selected.name
        )
        data_table_content = visualization_data_operations.get_data_content(
            test_selected.name, selected_projects_name
        )
        data_table_csv = get_data_table_csv(data_table_content)

        script, div = visualization_data(
            test_selected_tree, data_table_content, test_selected.name
        )

        # if data are missing we still have to send the info to the JS
        if script and div:
            plot = visualization_configuration_api.get_active_plot(test_selected.name)

            # Need to reinitialize custom value if plot object already created while a previous use of the feature
            plot = visualization_configuration_api.update_active_custom(
                plot.plot_name, test_selected.name, None
            )

            x_parameters = visualization_configuration_api.get_x_parameters(plot)
            y_parameters = visualization_configuration_api.get_y_parameters(plot)

        else:
            x_parameters, y_parameters = [], []

        data = {
            "data_table_csv": data_table_csv,
            "script": script,
            "div": div,
            "x_parameters": x_parameters,
            "y_parameters": y_parameters,
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type="application/javascript")


def update_configuration(request):
    """When a user selects a new x_parameter or y_parameter, this ajax is called to process the request and
    update the new axis

    Args:
        request:

    Returns: Update the plot

    """
    try:
        new_parameter = request.POST.get("new_parameter", None)
        parameter_type = request.POST.get("parameter_type", None)

        test_selected = selected_test_api.get_selected_test()
        plot = visualization_configuration_api.get_active_plot(test_selected.name)
        x_parameters = visualization_configuration_api.get_x_parameters(plot)
        y_parameters = visualization_configuration_api.get_y_parameters(plot)

        if parameter_type == "x_parameter":
            plot = visualization_configuration_api.update_active_x(
                test_selected.name, plot.plot_name, new_parameter
            )
            # Need to reinitialize custom value if plot object already created while a previous use of the feature
            plot = visualization_configuration_api.update_active_custom(
                plot.plot_name, test_selected.name, None
            )

        if parameter_type == "y_parameter":
            plot = visualization_configuration_api.update_active_y(
                test_selected.name, plot.plot_name, new_parameter
            )

        if parameter_type == "custom_parameter":
            plot = visualization_configuration_api.update_active_custom(
                plot.plot_name, test_selected.name, new_parameter
            )

        script, div = plots_operations.load_visualization(test_selected.name)

        data = {"script": script, "div": div}

        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type="application/javascript")


def update_custom_form(request):
    """Process a user request when he changes a custom parameter. That means a parameter that is not a x or y parameter.
    For instance, changing the element whose chemical composition is displayed on a piechart.

    Args:
        request:

    Returns:

    """
    test_selected = selected_test_api.get_selected_test()
    plot = visualization_configuration_api.get_active_plot(test_selected.name)

    if visualization_configuration_api.has_custom_param(plot):
        custom_parameters = visualization_configuration_api.get_custom_param(plot)
        active_x = visualization_configuration_api.get_active_x(plot)
        select_x = SelectXParameter(plot, active_x)

        select_custom = SelectCustomizedParameter(
            custom_parameters, "Select " + str(active_x)
        )
        context_custom = {
            "x_parameters": select_x,
            "customized_parameters": select_custom,
        }

        template = loader.get_template(
            "core_visualization_app/user/select_config_forms.html"
        )
        context = {}
        context.update(request)
        context.update(context_custom)

        return HttpResponse(
            json.dumps({"form": template.render(context)}),
            content_type="application/javascript",
        )

    else:
        return HttpResponse(json.dumps({}), "application/javascript")


def get_data_table_csv(data_table_list):
    """Convert a two dimensional list to a CSV table

    Args:
        data_table_list: two dimensional list

    Returns: CSV file

    """
    # Check if file already exists
    if path.isfile("./table.csv"):
        remove("./table.csv")

    # Create table
    with open("table" + ".csv", "w") as table:
        file_writer = csv.writer(
            table, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        for row in data_table_list:
            file_writer.writerow(row)
        table.close()
    with open("table" + ".csv", "r") as table:
        csv_table = table.read()
        table.close()

    return csv_table


def download_test_data(request):
    """Download the CSV file

    Args:
        request:

    Returns:

    """
    data_table_csv = request.POST.get("data_table_csv", None)
    return get_file_http_response(data_table_csv, "Data_table", "text/csv", "csv")


def visualization_data(test_selected_tree, data_table_content, test_selected_name):
    """Launch the loading of the plot

    Args:
        test_selected_tree:
        data_table_content:
        test_selected_name:

    Returns: html elements that are inserted in the template

    """
    plots_operations.set_plots(test_selected_tree, test_selected_name)
    script, div = plots_operations.load_visualization(
        test_selected_name, data_table_content
    )

    return script, div


def update_selection_forms(request):
    """

    Args:
        request:

    Returns:

    """
    if request.method == "GET":
        test_selected = selected_test_api.get_selected_test()
        plot = visualization_configuration_api.get_active_plot(test_selected.name)
        context_params = {}

        if visualization_configuration_api.get_plot_name(plot) == "Piechart":
            active_x = visualization_configuration_api.get_active_x(plot)
            select_x = SelectXParameter(plot, active_x, "Select a parameter:")
            custom_parameters = visualization_configuration_api.get_custom_param(plot)
            select_custom = SelectCustomizedParameter(
                custom_parameters, "Select " + str(active_x)
            )
            context_params = {
                "x_parameters": select_x,
                "customized_parameters": select_custom,
            }

        if visualization_configuration_api.get_plot_name(plot) in [
            "MultiBarchart",
            "ScatterGraph",
        ]:
            select_x = SelectXParameter(plot)
            context_params = {
                "x_parameters": select_x,
            }

        if visualization_configuration_api.get_plot_name(plot) in [
            "Boxplot",
            "Barchart",
        ]:
            select_x = SelectXParameter(plot)
            select_y = SelectYParameter(plot)
            context_params = {
                "x_parameters": select_x,
                "y_parameters": select_y,
            }

        template = loader.get_template(
            "core_visualization_app/user/select_config_forms.html"
        )
        context = {}
        context.update(request)
        context.update(context_params)

        return HttpResponse(
            json.dumps({"template": template.render(context)}),
            content_type="application/javascript",
        )

    else:
        return HttpResponse(json.dumps({}), "application/javascript")
