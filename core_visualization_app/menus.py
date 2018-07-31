""" Add Visualization in main menu
"""

from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

from core_visualization_app.settings import VISUALIZATION_USER_MENU_NAME

Menu.add_item(
    "main", MenuItem(VISUALIZATION_USER_MENU_NAME, reverse("core_visualization_index"))
)

