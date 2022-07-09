from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from jinja2 import Environment, FileSystemLoader, Template

BASE_DIR = Path(__file__).parent

DOMAIN_NAME: str = "https://anuran-roy.github.io"

# Markdown configuration

MARKDOWN_EXTENSIONS: List = [
    "extra",
    "toc",
]
# Contains list of Markdown extensions to be used while processing markdown.
# Refer https://python-markdown.github.io/extensions/ for more details


# Templating configuration

TEMPLATE_NAME: str = "_default"  # You can try "alt" here as well

TEMPLATE_DIR: str = BASE_DIR.absolute() / f"templates/{TEMPLATE_NAME}/"


class TemplatingEnv:
    def __init__(
        self,
        follow_links: Optional[bool] = False,
        enable_async: Optional[bool] = False,
        enable_autoescape: Optional[bool] = False,
        *args: Optional[List],
        **kwargs: Optional[Dict],
    ) -> None:
        self.loader = FileSystemLoader(TEMPLATE_DIR, followlinks=follow_links)
        self.environment = Environment(
            loader=self.loader, enable_async=enable_async, autoescape=enable_autoescape
        )

    def render(self, verbose: Optional[bool] = True, location: str, context: Optional[Dict] = {}) -> str:
        required_template = self.environment.get_template(location)
        return required_template.render(**context)


TEMPLATE_ENV = TemplatingEnv()

# Mapping settings

DEFAULT_MAPPING: Dict[str, Any] = {
    "archetypes": {
        "posts": {"template": "post.html", "objects": []},
        "index.md": {"template": "index.html", "objects": []},
        "blog.md": {"template": "blog.html", "objects": []},
        "_default": {"template": "_default.html", "objects": []},
    }
}

MAPPING: Dict = {}


def get_mapping() -> Dict:
    return DEFAULT_MAPPING if MAPPING == {} else MAPPING
