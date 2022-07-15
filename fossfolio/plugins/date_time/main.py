"""Every plugin must have a main.py file having the required run() method that can act as a controller.

The run() method MAY or MAY NOT receive any arguments or keyword arguments.

The run() method must return an object ( a string or a dictionary) from which value(s) will be injected during building.
"""
from datetime import datetime


def run(template_dict: dict, *args, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    template_dict["content"] = template_dict["content"].replace(r"<% current_time %>", current_time)

    return template_dict
