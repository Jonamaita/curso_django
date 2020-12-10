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


def sorted_numbers(request):
    """
    sorted view
    """
    numbers = request.GET["numbers"]
    numbers = map(int, numbers.split(","))
    numbers = sorted(numbers)
    data = {
        'status': 'ok',
        'numbers': numbers,
        "message": "Integers sorted successfully",

    }
    response = json.dumps(data, indent=4)
    return HttpResponse(response, content_type='application/json')


def say_hi(request, name, age):  # pylint: disable = unused-argument
    """
    view say_hi
    """
    if age < 12:
        message = f"Sorry {name}, you are not allowed here"
    else:
        message = f"Hello {name}!, Welcome to Platzigram!"

    return HttpResponse(message)
