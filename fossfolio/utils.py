from bs4 import BeautifulSoup


def prettify_html(html_string: str) -> str:
    return BeautifulSoup(html_string, "html.parser").prettify()
