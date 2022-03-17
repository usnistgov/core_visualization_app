"""Visualization models
"""
from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from core_visualization_app.permissions import rights


class Visualization(models.Model):
    class Meta(object):
        verbose_name = "core_visualization_app"
        default_permissions = ()
        permissions = (
            (
                rights.visualization_access,
                get_formatted_name(rights.visualization_access),
            ),
        )
