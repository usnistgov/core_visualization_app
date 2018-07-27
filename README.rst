======================
Core Visualization App
======================

Visualization feature for the curator core project.


Configuration
=============

1. Add "core_visualization_app" to your INSTALLED_APPS setting like this
------------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_visualization_app",
    ]

2. Include the core_visualization_app URLconf in your project urls.py like this
-------------------------------------------------------------------------------

.. code:: python

    url(r'^', include("core_visualization_app.urls")),
