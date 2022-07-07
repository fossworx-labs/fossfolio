from pathlib import Path
import os
from markdown import markdown
from plugins import inject
from typing import Optional, Dict, List, Tuple
from rich import print as rich_print
import shutil
import glob
import time
from config import BASE_DIR
from sitemap import generate_sitemap

# print(BASE_DIR.resolve())


def parse_md(md_string):
    # md = ""
    # with open(md_file, "r") as f:
    #     md = f.read()
    # return markdown(md)
    return markdown(md_string)


def collect_static() -> None:
    rich_print("[bold italic green]Collecting static assets...[/bold italic green]")
    shutil.rmtree(BASE_DIR / "build/assets", ignore_errors=True)
    shutil.copytree(BASE_DIR / "assets", BASE_DIR / "build/assets")

    count = len(list(glob.glob(str(BASE_DIR / "assets/*.*"), recursive=True)))

    rich_print(f"[bold italic]Collected {count} static assets[/bold italic]")


def excluded(
    filename: str,
    dirpath: str,
    exclude: Optional[List] = None,
    verbose: str = "True",
    *args: Optional[List],
    **kwargs: Optional[Dict],
) -> bool:
    """Handle files and directories to exclude. Returns True if file should be excluded."""
    supported_types: Tuple = ("md", "html")
    skip_dirs: Tuple = ("plugins", "templates", "build", "tests")

    if filename.split(".")[-1] not in supported_types:
        if verbose == "True":
            rich_print(
                f"[bold yellow]Skipping[/bold yellow] {dirpath}/{filename} as it is in unsupported format."
            )
        return True

    if dirpath.split("/")[1] in skip_dirs:
        if verbose == "True":
            rich_print(
                f"[bold yellow]Skipping[/bold yellow] {dirpath}/{filename} as the directory {dirpath} is to be skipped"
            )
        return True

    if exclude is not None and dirpath in exclude:
        if verbose == "True":
            rich_print(
                f"[bold yellow]Skipping[/bold yellow] {dirpath} as it is in exclude list."
            )
        return True

    rich_print(f"[bold green]Parsing[/bold green] {dirpath}/{filename}")
    return False


def list_files(
    exclude: Optional[List] = None, *args: Optional[List], **kwargs: Optional[Dict]
) -> Dict[str, str]:
    """Parses all supported document files and returns a mapping of file paths to file contents."""
    path_dict: Dict[str, str] = {}
    listOfFiles: Optional[List] = []

    base = Path(".")
    for (dirpath, dirnames, filenames) in os.walk(base):
        listOfFiles += [
            base / os.path.join(dirpath, filename)
            for filename in filenames
            if not excluded(filename, dirpath, exclude, *args, **kwargs)
        ]

    for i in listOfFiles:
        with open(i.absolute(), "r") as f:
            path_dict[str(i)] = f.read()

    parsed_markdown: Dict[str, str] = inject.inject(path_dict)

    for i in parsed_markdown:
        parsed_markdown[i] = parse_md(parsed_markdown[i])

    return parsed_markdown


def write_html(
    html_code: str = "",
    html_file_location: str = "",
    with_template: bool = False,
    templated_context: Dict = {},
) -> None:
    if not os.path.exists(html_file_location):
        os.makedirs(
            name=html_file_location[: html_file_location.rindex("/")], exist_ok=True
        )

    if with_template:
        pass  # Write the template embedding logic here.

    with open(html_file_location, "w") as f:
        f.write(html_code)


def build(sitemap: bool = True) -> None:
    start_time = time.time()
    shutil.rmtree(BASE_DIR / "build/", ignore_errors=True)

    files_dict = list_files(exclude=["templates"])

    for i in files_dict:
        write_html(
            html_code=files_dict[i],
            html_file_location=f"{BASE_DIR}/build/{i[:i.rindex('.')]}.html",
        )

    collect_static()

    if sitemap:
        generate_sitemap()

    end_time = time.time()

    rich_print(f"[bold blue]Build completed in {end_time - start_time}s[/bold blue]")


if __name__ == "__main__":
    build()
