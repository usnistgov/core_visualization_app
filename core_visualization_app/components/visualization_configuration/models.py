"""
Visualization configuration models
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors


class Plot(Document):
    session_id = fields.StringField(blank=False)
    test_name = fields.StringField(blank=False)
    default_plot = fields.BooleanField(blank=False)
    plot_name = fields.StringField(blank=False)
    plots_types = fields.ListField(blank=True)
    x_parameters = fields.ListField(blank=False)
    y_parameters = fields.ListField(blank=False)
    xy_values = fields.DictField(blank=True)
    custom_parameters = fields.ListField(blank=True)
    active_custom = fields.StringField(blank=True)

    @staticmethod
    def set_plots(
        session_id, plot_name, default, x_parameters, y_parameters, test_name
    ):
        """If plot already exists for the session we get it, otherwise it is created and saved.
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
        try:
            plot = Plot.objects.get(
                session_id=session_id,
                plot_name=plot_name,
                default_plot=default,
                x_parameters=x_parameters,
                y_parameters=y_parameters,
                test_name=test_name,
            )
        except mongoengine_errors.DoesNotExist as e:
            plot = Plot(
                session_id=session_id,
                plot_name=plot_name,
                default_plot=default,
                x_parameters=x_parameters,
                y_parameters=y_parameters,
                test_name=test_name,
            ).save()
        if plot_name not in plot.plots_types:
            if plot.plots_types:
                Plot.objects.filter(
                    session_id=session_id, test_name=test_name, plot_name=plot_name
                ).update(
                    plots_types=plot.plots_types.append(plot_name),
                )
            else:
                Plot.objects.filter(
                    session_id=session_id, test_name=test_name, plot_name=plot_name
                ).update(plots_types=[plot_name])
        return plot

    @staticmethod
    def delete_session_plots(session_id):
        """Delete all the plots objects associated to the session
        Args:
            session_id:
        Returns:

        """
        try:
            return Plot.objects.filter(session_id=str(session_id)).delete()
        except:
            return

    @staticmethod
    def delete_plots():
        """Delete all the plots objects

        Returns:

        """

        return Plot.objects.all().delete()

    @staticmethod
    def get_plot(session_id, test_name):
        """Return the only one active plot with the according test name for the session

        Args:
            session_id:
            test_name:

        Returns:

        """

        return Plot.objects.get(
            session_id=session_id, test_name=test_name, default_plot=True
        )

    @staticmethod
    def get_custom_param(plot):
        """Return the custom parameters list which is the parameters list used for special types of plots

        Args:
            plot:

        Returns:

        """
        return plot.custom_parameters

    @staticmethod
    def get_plot_name(plot):
        """Return the plot name

        Args:
            plot:

        Returns:

        """
        return plot.plot_name

    @staticmethod
    def get_x_parameters(plot):
        """Return the plot x parameters list

        Args:
            plot:

        Returns:

        """
        return plot.x_parameters

    @staticmethod
    def get_y_parameters(plot):
        """Return the plot x parameters list

        Args:
            plot:

        Returns:

        """
        return plot.y_parameters

    @staticmethod
    def is_plot(session_id, test_name):
        """Return True for the session if a plot exists that gets the given argument as test name

        Args:
            session_id:
            test_name:

        Returns:

        """
        if Plot.objects.filter(session_id=session_id, test_name=test_name):
            return True
        return False

    @staticmethod
    def has_custom_param(plot):
        """Return True if a plot gets an instantiate 'custom_parameters' field

        Args:
            plot:

        Returns:

        """
        if plot.custom_parameters:
            return True
        return False

    @staticmethod
    def update_custom_parameters(session_id, plot_name, test_name, custom_parameters):
        """Update for a session the custom parameters field of plot and return the plot

        Args:
            session_id:
            plot_name:
            test_name:
            custom_parameters:

        Returns:

        """
        Plot.objects.filter(
            session_id=session_id, test_name=test_name, plot_name=plot_name
        ).update(custom_parameters=custom_parameters)
        return Plot.get_plot(session_id, test_name)

    @staticmethod
    def has_xy_values(plot):
        """Return True if a plot gets an instantiate 'xy_values' field

        Args:
            plot:

        Returns:

        """
        if plot.xy_values:
            return True
        return False

    @staticmethod
    def get_xy_values(plot):
        """Return the dict of all possible combination of x and y parameters which are like [xa, xb, xc,..] and [ya, yb,..]
        xy_value: {xaya: [{xa: value1x, ya:value1y}, {xa: value2x, ya: value2y},..], xayb: ...}

        Args:
            plot:

        Returns:

        """
        return plot.xy_values

    @staticmethod
    def update_plot_xy_values(session_id, plot_name, test_name, xy_values):
        """Update the xy_values field of plot and return the plot

        Args:
            session_id:
            plot_name:
            test_name:
            xy_values:

        Returns:

        """
        Plot.objects.filter(
            session_id=session_id, test_name=test_name, plot_name=plot_name
        ).update(xy_values=xy_values)
        return Plot.get_plot(session_id, test_name)

    @staticmethod
    def update_active_custom(session_id, plot_name, test_name, active_custom):
        """Update the active custom field of plot and return the plot

        Args:
            session_id:
            plot_name:
            test_name:
            active_custom:

        Returns:

        """

        Plot.objects.filter(
            session_id=session_id, test_name=test_name, plot_name=plot_name
        ).update(active_custom=active_custom)
        return Plot.get_active_plot(session_id, test_name)
