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
    verbose: Optional[bool] = False,
    metadata: Optional[Dict[str, Any]] = {},
    attributes: Dict[str, Any] = {},
) -> str:
    """The method where the mappings are actually
    applied with different archetypes of content.
    """

    rendered_output = TEMPLATE_ENV.render(
        location=mapping["template"], context={"content": html_string, **contexts, "metadata": metadata, "attributes": attributes}
    )

    if verbose:
        rich_print(
            f"\n\n\n{__file__} > apply_mapping: HTML String received is of length = \n\n\n",
            len(html_string),
        )

        # rich_print(
        #     f"Rendered html string with mapping {mapping}. Length of string: {len(a)}"
        # )
        
        rich_print(f"Attributes = {attributes}")
        
    return prettify_html(rendered_output)


def wrap_template(
    html_string: str = "",
    location: str = "",
    verbose: Optional[bool] = False,
    attributes: Optional[Dict[str, Any]] = {},
    metadata: Dict[str, Any] = {},
    *args: Optional[List],
    **kwargs: Optional[Dict],
) -> Dict[str, Any]:
    """Get top-level html files from inside each template/theme folder.
    Then map them to the different content as defined by the mapping
    returned by get_mapping().
    """

    if verbose:
        rich_print(
            f"\n\n\n{__file__} > wrap_template: HTML String received from {location} = \n\n\n",
            html_string,
        )
        rich_print(html_string)
    # mapping: Dict[str, Any] = get_mapping().get("archetypes")

    TEMPLATE_PATTERN = f"{TEMPLATE_DIR.absolute()}/**/*.html"

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

    context_dict: Dict = {}
    if "context" in kwargs:
        context_dict = kwargs["contexts"]

    if verbose:
        rich_print(f"{len(html_string)}\t{detected_archetype_mapping}\t{context_dict}")
    return apply_mapping(
        html_string=html_string,
        mapping=detected_archetype_mapping,
        contexts=context_dict,
        metadata=metadata,
        attributes=attributes,
    )


if __name__ == "__main__":
    wrap_template(html_string="<p>{{ content }}</p>", location="_default")
