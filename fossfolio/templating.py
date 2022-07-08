from config import BASE_DIR, TEMPLATE_NAME, TEMPLATE_DIR, TEMPLATE_ENV, get_mapping
import glob
import os
from typing import Optional, Any, Dict, List
from rich import print as rich_print
import json
from utils import prettify_html


def auto_archetype(location: str = "") -> Dict[str, Any]:
    """Automatically detect the archetype of the content."""

    mapping: Dict[str, Any] = get_mapping().get("archetypes")

    archetype_possibilities: List[str] = reversed(location.split("/"))

    for i in archetype_possibilities:
        if i in mapping:
            return mapping[i]

    return mapping.get("_default")


def apply_mapping(
    html_string: str = None,
    mapping: Dict[str, Any] = {},
    contexts: Optional[Dict[str, Any]] = {},
) -> str:
    """The method where the mappings are actually
    applied with different archetypes of content.
    """

    return prettify_html(
        TEMPLATE_ENV.render(
            location=mapping["template"], context={"content": html_string, **contexts}
        )
    )


def wrap_template(
    html_string: str = "",
    location: str = "",
    verbose: bool = False,
    *args: Optional[List],
    **kwargs: Optional[Dict],
) -> Dict[str, Any]:
    """Get top-level html files from inside each template/theme folder.
    Then map them to the different content as defined by the mapping
    returned by get_mapping().
    """

    # mapping: Dict[str, Any] = get_mapping().get("archetypes")

    TEMPLATE_PATTERN = f"{TEMPLATE_DIR.absolute()}/*.html"

    files_list: List = list(glob.glob(TEMPLATE_PATTERN, recursive=True))

    # rich_print(files_list)

    if verbose:
        rich_print(
            f"[bold]Available archetypes for the template {TEMPLATE_NAME}[/bold]:"
        )
        for i in files_list:
            rich_print(f'- [green]{i[i.rindex("/")+1:]}[/green]')

        rich_print(f"\n[bold]Mapping detected for location: [/bold]{location}")
        rich_print(json.dumps(auto_archetype(location=location), indent=4))

    detected_archetype_mapping: Dict[str, str] = auto_archetype(location=location)

    return apply_mapping(html_string=html_string, mapping=detected_archetype_mapping)


if __name__ == "__main__":
    wrap_template(html_string="<p>{{ content }}</p>", location="_default")
