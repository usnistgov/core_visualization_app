""" Initialize permissions for core schema viewer app
"""
import logging

from django.contrib.auth.models import Group, Permission

import core_main_app.permissions.rights as main_rights
import core_visualization_app.permissions.rights as visualization_rights

logger = logging.getLogger(__name__)


def init_permissions():
    """Initialization of groups and permissions.

    Returns:

    """
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(
            name=main_rights.default_group
        )

        # Get visualization permissions
        visualization_access_perm = Permission.objects.get(
            codename=visualization_rights.visualization_access
        )

        # Add permissions to default group
        default_group.permissions.add(visualization_access_perm)

    except Exception as e:
        logger.error(str(e))
