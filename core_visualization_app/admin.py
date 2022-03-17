""" Url router for the administration site
"""
from django.urls import re_path
from django.contrib import admin

from core_visualization_app.views.admin import ajax as admin_ajax
from core_visualization_app.views.admin import views as admin_views

admin_urls = [
    re_path(
        r"^visualization$",
        admin_views.manage_visualization_data,
        name="core_visualization_app_manage_data",
    ),
    re_path(
        r"^visualization/build-visualization-data$",
        admin_ajax.build_visualization_data,
        name="core_visualization_app_build_data",
    ),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
