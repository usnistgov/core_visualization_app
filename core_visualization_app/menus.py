""" Add Visualization in main menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

from core_visualization_app.settings import VISUALIZATION_USER_MENU_NAME

Menu.add_item(
    "main", MenuItem(VISUALIZATION_USER_MENU_NAME, reverse("core_visualization_index"))
)

visualization_children = (
    MenuItem("Manage visualization data", reverse("admin:core_visualization_app_manage_data"), icon="list"),
)

Menu.add_item(
    "admin", MenuItem("DATA VISUALIZATION", None, children=visualization_children)
)


