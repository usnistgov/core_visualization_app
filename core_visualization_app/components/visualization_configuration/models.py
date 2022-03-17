"""
Visualization configuration models
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors


class Plot(Document):
    test_name = fields.StringField(blank=False)
    default_plot = fields.BooleanField(blank=False)
    plot_name = fields.StringField(blank=False)
    plots_types = fields.ListField(blank=True)
    active_x = fields.StringField(blank=False)
    active_y = fields.StringField(blank=False)
    active_custom = fields.StringField(blank=True)
    x_parameters = fields.ListField(blank=False)
    y_parameters = fields.ListField(blank=False)
    xy_values = fields.DictField(blank=True)
    custom_parameters = fields.ListField(blank=True)

    @staticmethod
    def set_plots(plot_name, default, x_parameters, y_parameters, test_name):
        """If plot already exists we get it, otherwise it is created and saved.
        Then, we need to update the plot types list if the plot does not belong to it.
        and return the plot

        Args:
            plot_name:
            default:
            x_parameters:
            y_parameters:
            test_name:

        Returns:

        """
        try:
            plot = Plot.objects.get(
                plot_name=plot_name,
                default_plot=default,
                x_parameters=x_parameters,
                y_parameters=y_parameters,
                active_x=x_parameters[0],
                active_y=y_parameters[0],
                test_name=test_name,
            )
        except mongoengine_errors.DoesNotExist as e:
            plot = Plot(
                plot_name=plot_name,
                default_plot=default,
                x_parameters=x_parameters,
                y_parameters=y_parameters,
                active_x=x_parameters[0],
                active_y=y_parameters[0],
                test_name=test_name,
            ).save()

        if plot_name not in plot.plots_types:
            if plot.plots_types:
                Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
                    plots_types=plot.plots_types.append(plot_name),
                    active_x=x_parameters[0],
                )
            else:
                Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
                    plots_types=[plot_name], active_x=x_parameters[0]
                )

        return plot

    @staticmethod
    def delete_plots():
        """Delete all the plots objects

        Returns:

        """
        return Plot.objects.all().delete()

    @staticmethod
    def get_active_plot(test_name):
        """Return the only one active plot with the according test name

        Args:
            test_name:

        Returns:

        """
        return Plot.objects.get(test_name=test_name, default_plot=True)

    @staticmethod
    def get_active_x(plot):
        """Return the active x which is a parameter belonging to the x parameters list

        Args:
            plot:

        Returns:

        """
        return plot.active_x

    @staticmethod
    def get_active_y(plot):
        """Return the active y which is a parameter belonging to the y parameters list

        Args:
            plot:

        Returns:

        """
        return plot.active_y

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
    def get_active_custom(plot):
        """Return the active custom parameter which belongs to the custom parameters list

        Args:
            plot:

        Returns:

        """
        return plot.active_custom

    @staticmethod
    def get_y_parameters(plot):
        """Return the plot x parameters list

        Args:
            plot:

        Returns:

        """
        return plot.y_parameters

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
    def update_active_x(test_name, plot_name, active_x):
        """Update the active x parameter. It remains one of the x parameters list element and return the plot

        Args:
            test_name:
            plot_name:
            active_x:

        Returns:

        """
        Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
            active_x=active_x
        )
        return Plot.get_active_plot(test_name)

    @staticmethod
    def update_active_y(test_name, plot_name, active_y):
        """Update the active y parameter. It remains one of the y parameters list element and return the plot

        Args:
            test_name:
            plot_name:
            active_y:

        Returns:

        """
        Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
            active_y=active_y
        )
        return Plot.get_active_plot(test_name)

    @staticmethod
    def is_plot(test_name):
        """Return True if a plot exists that gets the given argument as test name

        Args:
            test_name:

        Returns:

        """
        if Plot.objects.filter(test_name=test_name):
            return True
        return False

    @staticmethod
    def update_active_plot(test_name, plot_name):
        """Update the active plot. It remains one of the plot types list element and return the plot

        Args:
            test_name:
            plot_name:

        Returns:

        """
        Plot.objects.filter(test_name=test_name, default_plot=True).update(
            default_plot=False
        )
        Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
            default_plot=True
        )
        return Plot.get_active_plot(test_name)

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
    def update_plot_xy_values(plot_name, test_name, xy_values):
        """Update the xy_values field of plot and return the plot

        Args:
            plot_name:
            test_name:
            xy_values:

        Returns:

        """
        Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
            xy_values=xy_values
        )
        return Plot.get_active_plot(test_name)

    @staticmethod
    def update_custom_parameters(plot_name, test_name, custom_parameters):
        """Update the custom parameters field of plot and return the plot

        Args:
            plot_name:
            test_name:
            custom_parameters:

        Returns:

        """
        Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
            custom_parameters=custom_parameters
        )
        return Plot.get_active_plot(test_name)

    @staticmethod
    def update_active_custom(plot_name, test_name, active_custom):
        """Update the active custom field of plot and return the plot

        Args:
            plot_name:
            test_name:
            active_custom:

        Returns:

        """
        Plot.objects.filter(test_name=test_name, plot_name=plot_name).update(
            active_custom=active_custom
        )
        return Plot.get_active_plot(test_name)
