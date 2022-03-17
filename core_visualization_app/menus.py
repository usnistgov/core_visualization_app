""" Add Visualization in main menu
"""
from django.urls import reverse
from menu import Menu, MenuItem

visualization_children = (
    MenuItem(
        "Manage visualization data",
        reverse("admin:core_visualization_app_manage_data"),
        icon="list",
    ),
)

Menu.add_item(
    "admin", MenuItem("DATA VISUALIZATION", None, children=visualization_children)
)

Menu.add_item(
    "main", MenuItem("Data Visualization", reverse("core_visualization_index"))
)
