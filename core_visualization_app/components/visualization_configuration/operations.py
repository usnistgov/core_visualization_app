"""
Operations on visualization_configuration objects
"""
import json
from math import pi
from operator import truediv

import pandas
from bokeh.embed import components
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.transform import dodge

import core_explore_tree_app.components.data.query as query_database_api
import core_explore_tree_app.components.query_ontology.api as query_ontology_api
from core_visualization_app.components.visualization_configuration import (
    api as visualization_config_api,
)
import core_visualization_app.components.projects.api as projects_api
from core_visualization_app.utils import dict as dict_utils


def load_all_dicts(data_table, plot):
    """Return a dict of each combination possible of xy with their
    related data : {xaya: [{xa: value1x, ya:value1y}, {xa: value2x, ya: value2y},..], xayb: ...}

    Args:
        data_table:
        plot:

    Returns:

    """
    xy_all_dicts = {}

    for x in plot.x_parameters:
        for y in plot.y_parameters:
            y = str(y)
            x_index = None
            y_index = None

            for elt in data_table[0]:
                if elt == x:
                    x_index = data_table[0].index(elt)
                if elt == y:
                    y_index = data_table[0].index(elt)

            xy_all_dicts[x + y] = []
            for i in range(1, len(data_table)):
                if data_table[i][x_index] and data_table[i][y_index]:
                    xy_all_dicts[x + y].append(
                        {x: data_table[i][x_index], y: data_table[i][y_index]}
                    )

    return xy_all_dicts


def load_visualization(test_name, data_table=None):
    """Return script, div two html strings that will be inserted within the view.

    Args:
        test_name:
        data_table:

    Returns:

    """
    if visualization_config_api.is_plot(test_name):
        plot = visualization_config_api.get_active_plot(test_name)
    else:
        return None, None

    if not visualization_config_api.has_xy_values(plot):
        if not data_table:
            return None, None
        xy_all_dicts = load_all_dicts(data_table, plot)
        plot = visualization_config_api.update_plot_xy_values(
            plot.plot_name, plot.test_name, xy_all_dicts
        )

    else:
        xy_all_dicts = visualization_config_api.get_xy_values(plot)

    if plot.plot_name == "Piechart":
        active_custom = visualization_config_api.get_active_custom(plot)
        visualization_plot = pie_chart(xy_all_dicts, plot, active_custom)
    if plot.plot_name == "MultiBarchart":
        visualization_plot = multi_barchart(xy_all_dicts, plot)
    if plot.plot_name == "ScatterGraph":
        visualization_plot = scatter_graph(xy_all_dicts, plot)
    if plot.plot_name == "Boxplot":
        visualization_plot = box_plot(xy_all_dicts, plot)
    if plot.plot_name == "Barchart":
        visualization_plot = bar_chart(xy_all_dicts, plot)

    if visualization_plot:
        script, div = components(visualization_plot)
    else:
        return None, None

    return script, div


def multi_barchart(xy_all_dicts, plot):
    """Build a multibar chart and return the plot or None
    if there is no sufficient data to build the plot

    Args:
        xy_all_dicts:
        plot:

    Returns:

    """
    active_x = visualization_config_api.get_active_x(plot)
    y_parameters = visualization_config_api.get_y_parameters(plot)

    x_range = []

    all_colors = [
        "#1f77b4",
        "#aec7e8",
        "#ff7f0e",
        "#ffbb78",
        "#2ca02c",
        "#98df8a",
        "#d62728",
        "#ff9896",
        "#9467bd",
        "#c5b0d5",
        "#8c564b",
        "#c49c94",
        "#e377c2",
        "#f7b6d2",
        "#7f7f7f",
        "#c7c7c7",
        "#bcbd22",
        "#dbdb8d",
        "#17becf",
        "#9edae5",
    ]

    for i in range(0, len(y_parameters)):
        xy_dict = xy_all_dicts[active_x + y_parameters[i]]
        for couple in xy_dict:
            if couple[active_x] not in x_range:
                x_range.append(couple[active_x])

    if not x_range:
        return None

    width = configure_plot_width(x_range, 200 + 200 * len(x_range))

    p = figure(
        x_range=x_range,
        plot_height=600,
        plot_width=width,
        title="Nested bar chart - " + plot.test_name + " by " + active_x,
    )

    n = len(y_parameters)
    width = truediv(1, n) - 0.1

    for i in range(0, len(y_parameters)):
        xy_dict = xy_all_dicts[active_x + y_parameters[i]]
        classification = {}
        data = {"x_range": [], "y_data": []}
        for couple in xy_dict:
            if couple[active_x] in classification:
                if couple[y_parameters[i]]:

                    classification[couple[active_x]].append(
                        float(couple[y_parameters[i]])
                    )
            else:
                if couple[y_parameters[i]]:
                    classification[couple[active_x]] = [float(couple[y_parameters[i]])]
        color = all_colors[i]

        for k, v in list(classification.items()):
            classification[k] = truediv(sum(classification[k]), len(classification[k]))
            data["x_range"].append(k)
            data["y_data"].append(classification[k])

        y_name = y_parameters[i]

        if (i + 1) < truediv(n + 1, 2):
            step = truediv(i + 1, n) - truediv(2, n)
        if (i + 1) == truediv(n + 1, 2):
            step = 0
        if (i + 1) > truediv(n + 1, 2):
            step = truediv(i + 1, n) - truediv(2, n)

        source = ColumnDataSource(data=data)
        p.vbar(
            x=dodge("x_range", step, range=p.x_range),
            top="y_data",
            color=color,
            legend_label=y_name,
            width=width,
            source=source,
        )

        p.y_range.start = 0

    layout = column(p)

    return layout


def scatter_graph(xy_all_dicts, plot):
    """Build a scatter chart and return the plot or None
    if there is no sufficient data to build the plot

    Args:
        xy_all_dicts:
        plot:

    Returns:

    """
    active_x = visualization_config_api.get_active_x(plot)

    all_colors = [
        "#1f77b4",
        "#aec7e8",
        "#ff7f0e",
        "#ffbb78",
        "#2ca02c",
        "#98df8a",
        "#d62728",
        "#ff9896",
        "#9467bd",
        "#c5b0d5",
        "#8c564b",
        "#c49c94",
        "#e377c2",
        "#f7b6d2",
        "#7f7f7f",
        "#c7c7c7",
        "#bcbd22",
        "#dbdb8d",
        "#17becf",
        "#9edae5",
    ]

    x_range = []
    for i in range(0, len(plot.y_parameters)):
        xy_dict = xy_all_dicts[active_x + plot.y_parameters[i]]
        for couple in xy_dict:
            if couple[active_x] not in x_range:
                x_range.append(couple[active_x])

    if not x_range:
        return None

    width = configure_plot_width(x_range, 200 + 200 * len(x_range))

    p = figure(
        plot_height=600,
        plot_width=width,
        x_range=x_range,
        title="Scatter graph - " + plot.test_name + " by " + active_x,
    )

    for i in range(0, len(plot.y_parameters)):
        xy_dict = xy_all_dicts[active_x + plot.y_parameters[i]]
        data = {"x_data": [], "y_data": []}

        for couple in xy_dict:
            data["x_data"].append(couple[active_x])
            data["y_data"].append(float(couple[plot.y_parameters[i]]))

        color = all_colors[i]

        source = ColumnDataSource(data)
        y_name = plot.y_parameters[i]
        p.circle(
            x="x_data", y="y_data", color=color, source=source, legend_label=y_name
        )

    p.xaxis.axis_label = active_x
    layout = column(p)

    return layout


def bar_chart(xy_all_dicts, plot):
    """Build a bar chart and return the plot or None
    if there is no sufficient data to build the plot

    Args:
        xy_all_dicts:
        plot:

    Returns:

    """
    # load groups
    active_x = visualization_config_api.get_active_x(plot)
    active_y = visualization_config_api.get_active_y(plot)

    xy_dict = xy_all_dicts[active_x + active_y]

    if not xy_dict:
        return None

    x_data = []
    y_data = []

    for couple in xy_dict:
        x_data.append(couple[active_x])
        y_data.append(couple[active_y])

    x_groups = {}
    counter = {}

    x_axis = []
    y_axis = []

    for i in range(0, len(x_data)):
        if y_data[i]:
            if x_data[i] not in x_groups:
                x_groups[x_data[i]] = float(y_data[i])
                counter[x_data[i]] = 1
            else:
                x_groups[x_data[i]] += float(y_data[i])
                counter[x_data[i]] += 1

    for k, v in list(x_groups.items()):
        x_axis.append(k)
        y_axis.append(v / counter[k])

    source = ColumnDataSource(data=dict(x_axis=x_axis, y_axis=y_axis))

    width = configure_plot_width(x_axis, 200 + 200 * len(x_axis))

    p = figure(
        x_range=x_axis,
        plot_height=600,
        plot_width=width,
        title="Bar chart - " + plot.test_name + ": " + active_y + " by " + active_x,
    )

    p.vbar(x="x_axis", top="y_axis", source=source, width=0.8, bottom=0)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    layout = column(p)

    return layout


def pie_chart(xy_all_dicts, plot, x_value=None):
    """Build a pie chart and return the plot or None
    if there is no sufficient data to build the plot

    Args:
        xy_all_dicts:
        plot:
        x_value:

    Returns:

    """
    active_x = visualization_config_api.get_active_x(plot)

    # initialization of select button options
    active_x_values = []

    for i in range(0, len(plot.y_parameters)):
        if (active_x + plot.y_parameters[i]) in xy_all_dicts:
            xy_dict_list = xy_all_dicts[active_x + plot.y_parameters[i]]
            for elt in xy_dict_list:
                if elt[active_x] not in active_x_values:
                    active_x_values.append(
                        elt[active_x]
                    )  # active_x_values = list of all different project id if project id is active x

    plot = visualization_config_api.update_custom_parameters(
        plot.plot_name, plot.test_name, active_x_values
    )

    if x_value is None:
        x_value = active_x_values[0]  # Default value

    # initialization of the plot
    x = {}

    for j in range(0, len(plot.y_parameters)):
        y_data = []
        if (active_x + plot.y_parameters[j]) in xy_all_dicts:
            xy_dict_list = xy_all_dicts[active_x + plot.y_parameters[j]]
            for elt in xy_dict_list:
                if elt[active_x] == x_value:
                    if elt[plot.y_parameters[j]]:
                        y_data.append(float(elt[plot.y_parameters[j]]))
            if y_data:
                y_value = truediv(sum(y_data), len(y_data))
                x[plot.y_parameters[j]] = y_value

    if not x:
        return None

    data = (
        pandas.Series(x).reset_index(name="value").rename(columns={"index": "number"})
    )
    data["angle"] = data["value"] / data["value"].sum() * 2 * pi
    data["color"] = [
        "#1f77b4",
        "#aec7e8",
        "#ff7f0e",
        "#ffbb78",
        "#2ca02c",
        "#98df8a",
        "#d62728",
        "#ff9896",
        "#9467bd",
        "#c5b0d5",
        "#8c564b",
        "#c49c94",
        "#e377c2",
        "#f7b6d2",
        "#7f7f7f",
        "#c7c7c7",
        "#bcbd22",
        "#dbdb8d",
        "#17becf",
        "#9edae5",
    ][: len(x)]

    p = figure(
        plot_height=600,
        title="Pie Chart: " + plot.test_name + ": " + active_x + " - " + x_value,
        tools="hover",
        tooltips="@number: @value",
        x_range=(-0.5, 1.0),
    )
    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_label="number",
        source=data,
    )

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    layout = column(p)

    return layout


def box_plot(xy_all_dicts, plot):
    """Build a box plot and return the plot or None
    if there is no sufficient data to build the plot

    Args:
        xy_all_dicts:
        plot:

    Returns:

    """
    active_x = visualization_config_api.get_active_x(plot)
    active_y = visualization_config_api.get_active_y(plot)

    xy_dict = xy_all_dicts[active_x + active_y]

    if not xy_dict:
        return None

    x_axis = []
    y_axis = []

    for couple in xy_dict:
        x_axis.append(couple[active_x])
        y_axis.append(couple[active_y])

    # define which values belong to which build
    builds = x_axis
    cats = []
    max_len = 20

    score = y_axis

    for i in range(0, len(score)):
        if score[i]:
            if builds[i] not in cats:
                if len(builds[i]) > max_len:
                    max_len = len(builds[i])
                cats.append(builds[i])
            score[i] = float(score[i])

    df = pandas.DataFrame(dict(score=score, group=builds))

    # find the quartiles and IQR for each category
    groups = df.groupby("group")
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    groups_len = len(groups)

    width = configure_plot_width(groups, int(200 * groups_len * truediv(max_len, 20)))

    p = figure(
        plot_height=600,
        plot_width=width,
        background_fill_color="#EFE8E2",
        title="Box plot - "
        + plot.test_name
        + ": "
        + plot.active_y
        + " by "
        + plot.active_x,
        x_range=cats,
    )

    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.score = [
        min([x, y]) for (x, y) in zip(list(qmax.loc[:, "score"]), upper.score)
    ]
    lower.score = [
        max([x, y]) for (x, y) in zip(list(qmin.loc[:, "score"]), lower.score)
    ]

    # stems
    p.segment(cats, upper.score, cats, q3.score, line_color="black")
    p.segment(cats, lower.score, cats, q1.score, line_color="black")

    # boxes
    p.vbar(cats, 0.7, q2.score, q3.score, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q1.score, q2.score, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(cats, lower.score, 0.2, 0.0001, line_color="black")
    p.rect(cats, upper.score, 0.2, 0.0001, line_color="black")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size = "12pt"

    layout = column(p)

    return layout


def set_x_axis_parameters(list_of_dicts):
    """Load the x_parameters list related to a plot by using the ontology annotation part dedicated to this task
    We never need to query the database to get the x_parameters

    Args:
        list_of_dicts:

    Returns:

    """
    x_parameters = []

    for x_dict in list_of_dicts:
        x_parameters.append(x_dict["name"])

    return x_parameters


def set_y_axis_parameters(list_of_dicts, project_filter):
    """Load the y_parameters list related to a plot by using the ontology annotation part dedicated to this task
    We may need to query the database

    Args:
        list_of_dicts:
        project_filter:

    Returns:

    """
    active_ontology = query_ontology_api.get_active()
    template_id = active_ontology.template.id
    y_parameters = []

    if "queries" in list_of_dicts:
        list_of_dicts = list_of_dicts["queries"]
        y_list_of_list = []
        for query in list_of_dicts:
            query_filter = {query["query"]: "1"}
            path = query["query"]
            y_parameters_part = get_y_parameters(
                path, template_id, project_filter, query_filter
            )
            for i in range(0, len(y_parameters_part)):
                y_parameters_part[i] = str(y_parameters_part[i])

            y_list_of_list.append(y_parameters_part)

        # y_list_of_list == [['a','b'],['1','2','3']] -> y_parameters == ['a1', 'a2', 'b1', 'b2']
        for elt in y_list_of_list[0]:
            for i in range(0, len(y_list_of_list[1]) - 1):
                y_parameter = elt
                y_parameter += " " + y_list_of_list[1][i]
                y_parameters.append(y_parameter)

    if "query" in list_of_dicts:
        query_filter = {list_of_dicts["query"]: "1"}
        y_parameters = get_y_parameters(
            list_of_dicts["query"], template_id, project_filter, query_filter
        )

    if isinstance(list_of_dicts, list):
        if "name" in list_of_dicts[0]:
            for y_dict in list_of_dicts:
                y_parameters.append(y_dict["name"])

    return y_parameters


def get_y_parameters(path, template_id, project_filter, query_filter):
    """Query the database and return the list of the y_parameters related to a plot

    Args:
        path:
        template_id:
        project_filter:
        query_filter:

    Returns:

    """
    y_parameters = []
    for project in project_filter:
        results = query_database_api.execute_query(
            template_id, [json.dumps(project)], json.dumps(query_filter)
        )
        for result in results:
            list_of_dicts_param = dict_utils.get_list_inside_dict(
                path, result.dict_content
            )
            if list_of_dicts_param:
                for dict_param in list_of_dicts_param:
                    param_name = path.split(".")[-1]
                    if param_name in list(dict_param.keys()):
                        if dict_param[param_name] not in y_parameters:
                            if isinstance(dict_param[param_name], int):
                                if str(dict_param[param_name]) not in y_parameters:
                                    y_parameters.append(str(dict_param[param_name]))
                            else:
                                y_parameters.append(dict_param[param_name])
    return y_parameters


def set_plots(test_selected_tree, test_name):
    """Use the ontology annotation to set the python visualization configuration objects

    Args:
        test_selected_tree:
        test_name:

    Returns:

    """
    visualization_annotation = json.loads(
        test_selected_tree["annotations"]["visualization"]
    )
    plots_annotation = visualization_annotation[1]["data"]
    projects = projects_api.get_selected_projects_name()
    project_filter = []

    query = visualization_annotation[0]["project"]
    for project in projects:
        project_filter.append({query: project})

    # New visualization -> must reset all plots to avoid issues
    visualization_config_api.delete_plots()

    for plot_annotation in plots_annotation:
        default = False
        plot_name, x_parameters, y_parameters = "", [], []  # init

        for k, v in list(plot_annotation.items()):
            if k == "default":
                default = True
            if k == "Plot":
                plot_name = v
            if k == "X-axis":
                x_parameters = set_x_axis_parameters(v)
            if k == "Y-axis":
                y_parameters = set_y_axis_parameters(v, project_filter)

        if x_parameters and y_parameters:
            plot = visualization_config_api.set_plots(
                plot_name, default, x_parameters, y_parameters, test_name
            )

    return


def configure_plot_width(x_range, width):
    """Define the plot width according to the number of elements that have to be on the plot

    Args:
        x_range:
        width:

    Returns:

    """
    if len(x_range) > 2:
        width = width
    else:
        width = 600
    return width
