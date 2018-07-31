"""Visualization app user views
"""

from django.core.urlresolvers import reverse_lazy

from core_main_app.utils.rendering import render

import core_main_app.utils.decorators as decorators
import core_visualization_app.permissions.rights as rights


@decorators.permission_required(content_type=rights.visualization_content_type,
                                permission=rights.visualization_access, login_url=reverse_lazy("core_main_app_login"))
def index(request):
    """ Visualization app initial homepage

    :param request:
    :return:

    """
    return render(request, "core_visualization_app/user/visualization.html")
