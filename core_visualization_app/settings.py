"""Core Visualization App Settings
"""

from django.conf import settings

if not settings.configured:
    settings.configure()

# MENU
VISUALIZATION_USER_MENU_NAME = getattr(
    settings, "VISUALIZATION_USER_MENU_NAME", "Data Visualization"
)
CQL_NAMESPACE = getattr(settings, "CQL_NAMESPACE")
