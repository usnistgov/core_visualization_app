"""
Visualization configuration api
"""
from core_visualization_app.components.visualization_configuration.models import Plot


def set_plots(session_id, plot_name, default, x_parameters, y_parameters, test_name):
    """If plot already exists for the current session we get it, otherwise it is created and saved.
    Then, we need to update the plot types list if the plot does not belong to it.
    and return the plot

    Args:
        session_id:
        plot_name:
        default:
        x_parameters:
        y_parameters:
        test_name:

    Returns:

    """
    return Plot.set_plots(
        session_id, plot_name, default, x_parameters, y_parameters, test_name
    )


def get_plot(session_id, test_name):
    """Return the only one active plot with the according test name for the session

    Args:
        session_id:
        test_name:

    Returns:

    """
    return Plot.get_plot(session_id, test_name)


def is_plot(session_id, test_name):
    """Return True if a plot exists for the session that gets the given argument as test name

    Args:
        session_id:
        test_name:

    Returns:

    """
    return Plot.is_plot(session_id, test_name)


def get_x_parameters(plot):
    """Return the plot x parameters list

    Args:
        plot:

    Returns:

    """
    return Plot.get_x_parameters(plot)


def get_y_parameters(plot):
    """Return the plot x parameters list

    Args:
        plot:

    Returns:

    """
    return Plot.get_y_parameters(plot)


def delete_session_plots(session_id):
    """Delete all the plots objects associated to the current session
    Args:
        session_id:
    Returns:

    """
    return Plot.delete_session_plots(session_id)


def delete_plots():
    """Delete all the plots objects

    Returns:

    """
    return Plot.delete_plots()


def get_plot_name(plot):
    """Return the plot name

    Args:
        plot:

    Returns:

    """
    return Plot.get_plot_name(plot)


def update_custom_parameters(session_id, plot_name, test_name, custom_parameters):
    """Update the custom parameters field of plot and return the plot

    Args:
        session_id:
        plot_name:
        test_name:
        custom_parameters:

    Returns:

    """
    return Plot.update_custom_parameters(
        session_id, plot_name, test_name, custom_parameters
    )


def get_custom_param(plot):
    """Return the custom parameters list which is the parameters list used for special types of plots

    Args:
        plot:

    Returns:

    """
    return Plot.get_custom_param(plot)


def has_custom_param(plot):
    """Return True if a plot gets an instantiate 'custom_parameters' field

    Args:
        plot:

    Returns:

    """
    return Plot.has_custom_param(plot)


def has_xy_values(plot):
    """Return True if a plot gets an instantiate 'xy_values' field

    Args:
        plot:

    Returns:

    """
    return Plot.has_xy_values(plot)


def get_xy_values(plot):
    """Return the dict of all possible combination of x and y parameters which are like [xa, xb, xc,..] and [ya, yb,..]
    xy_value: {xaya: [{xa: value1x, ya:value1y}, {xa: value2x, ya: value2y},..], xayb: ...}

    Args:
        plot:

    Returns:

    """
    return Plot.get_xy_values(plot)


def update_plot_xy_values(session_id, plot_name, test_name, xy_values):
    """Update the xy_values field of plot and return the plot

    Args:
        session_id:
        plot_name:
        test_name:
        xy_values:

    Returns:

    """
    return Plot.update_plot_xy_values(session_id, plot_name, test_name, xy_values)


def update_active_custom(session_id, plot_name, test_name, active_custom):
    """Update the active custom field of plot and return the plot

    Args:
        session_id:
        plot_name:
        test_name:
        active_custom:

    Returns:

    """
    return Plot.update_active_custom(session_id, plot_name, test_name, active_custom)
