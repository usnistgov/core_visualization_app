""" Forms for user views
"""
from django import forms

from core_visualization_app.components.visualization_configuration import (
    api as visualization_config_api,
)


class SelectProjects(forms.Form):
    """Form to select projects to visualize"""

    projects = forms.MultipleChoiceField(
        label="Which project(s) would you like to explore the related data of?",
        required=True,
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self):
        super(SelectProjects, self).__init__()


class SelectTestCategory(forms.Form):
    """Form to select what Test Category to visualize"""

    categories = forms.ChoiceField(
        label="Which kind of testing data are you interested in?",
        required=True,
        widget=forms.RadioSelect(),
    )

    def __init__(self):
        super(SelectTestCategory, self).__init__()


class SelectTestSubcategory(forms.Form):
    """Form to select what Test Subcategory to visualize"""

    subcategories = forms.ChoiceField(
        label="Which test results would you like to see?",
        required=True,
        widget=forms.RadioSelect(),
    )

    def __init__(self):
        super(SelectTestSubcategory, self).__init__()


class SelectXParameter(forms.Form):
    """Form to select what Test Subcategory to visualize"""

    x_parameters = forms.ChoiceField(
        label="Change X-axis:", required=False, widget=forms.Select()
    )

    def __init__(self, plot=None, selected=None, label=None, *args):
        super(SelectXParameter, self).__init__(*args)
        if plot:
            x_parameters = visualization_config_api.get_x_parameters(plot)
            x_parameters_tuples = []
            for x_parameter in x_parameters:
                x_parameters_tuples.append((str(x_parameter), str(x_parameter)))
            self.fields["x_parameters"].choices = x_parameters_tuples
        if selected:
            self.fields["x_parameters"].initial = [selected]
        if label:
            self.fields["x_parameters"].label = label


class SelectYParameter(forms.Form):
    """Form to select what Test Subcategory to visualize"""

    y_parameters = forms.ChoiceField(
        label="Change Y-axis:", required=False, widget=forms.Select()
    )

    def __init__(self, plot=None, *args):
        super(SelectYParameter, self).__init__(*args)
        if plot:
            y_parameters_tuples = []
            y_parameters = visualization_config_api.get_y_parameters(plot)
            for y_parameter in y_parameters:
                y_parameters_tuples.append((str(y_parameter), str(y_parameter)))

            self.fields["y_parameters"].choices = y_parameters_tuples


class SelectCustomizedParameter(forms.Form):
    """Form to select what Test Subcategory to visualize"""

    customized_parameters = forms.ChoiceField(
        label="", required=False, widget=forms.Select()
    )

    def __init__(self, parameters=None, label="", *args):
        super(SelectCustomizedParameter, self).__init__(*args)
        if parameters:
            customized_parameters_tuples = []
            for customized_parameter in parameters:
                customized_parameters_tuples.append(
                    (str(customized_parameter), str(customized_parameter))
                )

            self.fields["customized_parameters"].choices = customized_parameters_tuples
            self.fields["customized_parameters"].label = label
