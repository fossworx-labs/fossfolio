from bs4 import BeautifulSoup
import platform
from pathlib import Path
from typing import Optional
from rich import print as rich_print

def prettify_html(html_string: str) -> str:
    return BeautifulSoup(html_string, "html.parser").prettify()


def get_platform_delimiter() -> str:
    detected_platform: str = platform.system()
    if detected_platform == "Windows":
        return "\\"
    elif detected_platform in {"Linux", "Darwin"}:
        return "/"

def get_html_path(path_string: str, verbose: Optional[bool] = False) -> str:
    DELIMITER: str = get_platform_delimiter()
    directory: str = DELIMITER.join(path_string.split(DELIMITER)[:-1])

    if verbose:
        rich_print(f"\n\n\n\nDirectory = {directory}\n\n")

    if directory[:7] == "content":
        directory = directory[7:]

    file_name: str = path_string.split(DELIMITER)[-1].split(".")[0]
    
    new_path: str = f"{directory}/{file_name}.html".replace(" ", "-")
    
    if verbose:
        rich_print(file_name)
        rich_print(f"\n\n\n\nNew Path = {new_path}\n\n")

    return new_path.lower()

if __name__ == "__main__":
    assert(get_platform_delimiter() == "/")
    print(get_html_path("content/test.md", verbose=True))
    assert(get_html_path("content/test.md", verbose=True) == "/test.html")
    print(get_html_path("content/content2/posts/hello there.md", verbose=True))
    assert(get_html_path("content/content2/posts/hello there.md", verbose=True) == "/content2/posts/hello-there.html")
    print(get_html_path("content/test.md", verbose=True))
    assert(get_html_path("content/test.md", verbose=True) == "/test.html")
    print(get_html_path("content/test.md", verbose=True))
    assert(get_html_path("content/test.md", verbose=True) == "/test.html")
    