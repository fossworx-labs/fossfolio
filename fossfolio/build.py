from pathlib import Path
import os
from markdown import markdown
from plugins import inject
from typing import Optional, Dict, List, Tuple
from rich import print as rich_print
import shutil
import glob
import time
from config import MARKDOWN_EXTENSIONS, MARKDOWN_INSTANCE
from sitemap import generate_sitemap
from slugify import slugify

from templating import wrap_template

import sys

BASE_DIR = Path(__file__).parent

if BASE_DIR not in sys.path:
    print(f"Added {BASE_DIR} to sys.path")
    sys.path.append(BASE_DIR.absolute())

# print(BASE_DIR.resolve())


def parse_md(md_string):
    # md = ""
    # with open(md_file, "r") as f:
    #     md = f.read()
    # return markdown(md)
    return MARKDOWN_INSTANCE.render(md_string)


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

    scan_dirs: Tuple = ("assets", "content")

    if filename.split(".")[-1] not in supported_types:
        if verbose == "True":
            rich_print(
                f"[bold yellow]Skipping[/bold yellow] {dirpath}/{filename} as it is in unsupported format."
            )
        return True

    if dirpath.split("/")[1] not in scan_dirs:
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
    exclude: Optional[List] = None,
    verbose: Optional[bool] = False,
    *args: Optional[List],
    **kwargs: Optional[Dict],
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
        path_dict[str(i)] = open(i.absolute(), "r").read()
        if verbose:
            rich_print("Reading file ", i.absolute())
            rich_print(path_dict[str(i)])

    parsed_markdown: Dict[str, Any] = inject.inject(path_dict)

    for i in parsed_markdown:
        parsed_markdown[i] = parse_md(parsed_markdown[i])
        if verbose:
            rich_print("\n\nParsed HTML ", i)
            rich_print(parsed_markdown[str(i)])

    return parsed_markdown


def write_html(
    html_code: str = "",
    html_file_location: str = "",
    templated_context: Dict = {},
    verbose: Optional[bool] = False,
) -> None:
    """Writes the provided HTML templated code to the build folder."""
    html_file_location = html_file_location.replace("/build/content/", "/build/")

    if verbose:
        rich_print(f"Writing {html_code[:10]}... to {html_file_location}")

    if not os.path.exists(html_file_location):
        os.makedirs(
            name=html_file_location[: html_file_location.rindex("/")], exist_ok=True
        )

    with open(html_file_location, "w") as f:
        f.write(html_code)


def build(
    sitemap: bool = True,
    with_template: bool = False,
    verbose: Optional[bool] = False,
) -> None:
    start_time = time.time()
    shutil.rmtree(BASE_DIR / "build/", ignore_errors=True)

    files_dict = list_files(exclude=["templates"])

    if with_template:
        # Write the template embedding logic here.
        for i in files_dict:
            files_dict[i] = wrap_template(
                html_string=files_dict[i][1], metadata=files_dict[i][0], location=i
            )

    for i in files_dict:
        if verbose:
            rich_print(f"files_dict.{i} = {files_dict[i][:10]}")
        write_html(
            html_code=files_dict[i],
            html_file_location=f"{BASE_DIR}/build/{i[:i.rindex('/')]}/{slugify(i[i.rindex('/'):i.rindex('.')])}.html",
        )

    collect_static()

    if sitemap:
        generate_sitemap()

    end_time = time.time()

    rich_print(f"[bold blue]Build completed in {end_time - start_time}s[/bold blue]")


if __name__ == "__main__":
    build(with_template=True)
