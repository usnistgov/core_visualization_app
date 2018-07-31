""" Url router for the schema viewer application
"""

from django.conf.urls import url

import core_visualization_app.views.user.views as user_views

urlpatterns = [
    url(r'^$', user_views.index,
        name='core_visualization_index'),
]
