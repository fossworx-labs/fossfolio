"""Every plugin must have a main.py file having the required run() method
that can act as a controller.

The run() method MAY or MAY NOT receive any arguments or keyword arguments.

The run() method must return an object ( a string or a dictionary) from which
value(s) will be injected during building.
"""


def run(template_str: str, *args, **kwargs) -> str:
    return template_str
