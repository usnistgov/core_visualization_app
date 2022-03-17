""" Visualization admin views
"""
from django.contrib.admin.views.decorators import staff_member_required

from core_main_app.utils.rendering import admin_render


@staff_member_required
def manage_visualization_data(request):
    """

    Args:
        request:

    Returns:  view with buttons to  manage visualization data

    """
    assets = {
        "js": [
            {
                "path": "core_visualization_app/admin/js/build_visualization_data.js",
                "is_raw": False,
            }
        ]
    }

    return admin_render(
        request,
        "core_visualization_app/admin/manage_visualization_data.html",
        assets=assets,
    )
