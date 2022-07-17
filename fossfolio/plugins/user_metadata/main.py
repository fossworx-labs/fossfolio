"""Every plugin must have a main.py file having the required run() method that can act as a controller.

The run() method MAY or MAY NOT receive any arguments or keyword arguments.

The run() method must return an object ( a string or a dictionary) from which value(s) will be injected during building.
"""

import socket


def run(template_dict: dict, *args, **kwargs):
    user = socket.gethostname()
    template_dict["content"] = template_dict["content"].replace(r"<% user %>", user)
    
    return template_dict
