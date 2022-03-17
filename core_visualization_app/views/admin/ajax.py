""" Admin Ajax visualization
"""

from django.http import HttpResponse
import core_visualization_app.tasks as visualization_tasks
import json


def build_visualization_data(request):
    """Build data table object asynchronously

    Args:
        request:

    Returns:

    """
    # start asynchronous task
    # FIXME: There is actually no feedback for the user to let him know when the data are ready
    visualization_tasks.build_visualization_data.delay()
    return HttpResponse(json.dumps({}), content_type="application/javascript")
