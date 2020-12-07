"""
views
"""
import json
# Utilitys
from datetime import datetime

# Django
from django.http import HttpResponse


def hello_world(request):  # pylint: disable = unused-argument
    """
    View hello world
    """
    now = datetime.now().strftime("%b %dth, %Y - %H:%M hrs")
    return HttpResponse(f"Oh, hi! Current server time is {now}")


def numbers(request):
    """
    View numbers
    """
    get_numbers = request.GET["numbers"]
    get_numbers = map(int, get_numbers.split(","))
    get_numbers = sorted(get_numbers)
    response = json.dumps({"numbers": get_numbers}, indent=4)
    return HttpResponse(response)
