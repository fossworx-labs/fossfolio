from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
import yaml
import os
import sys
from utils import get_platform_delimiter

DELIMITER: str = get_platform_delimiter()  # Platform specific delimiter.

BASE_DIR = Path(__file__).parent

if BASE_DIR not in sys.path:
    print(f"Added {BASE_DIR} to sys.path")
    sys.path.append(BASE_DIR.absolute())

DOMAIN_NAME: str = "https://anuran-roy.github.io"

# Markdown configuration

MARKDOWN_EXTENSIONS: List = [
    "meta",
    "extra",
    "toc",
]
# Contains list of Markdown extensions to be used while processing markdown.
# Refer https://python-markdown.github.io/extensions/ for more details


class MarkdownRenderer:
    def __init__(self, extensions: List = MARKDOWN_EXTENSIONS):
        self.extensions = extensions
        self.instance = Markdown(extensions=extensions)

    def render(self, text: str) -> Tuple[Dict[str, Any], str]:
        """Returns dictionary containing metadata to be processed,
        along with the rendered standard markdown
        """
        rendered_output = self.instance.convert(text)
        metadata: Dict = {}
        if "meta" in self.extensions:
            metadata = self.instance.Meta
        return (metadata, rendered_output)


MARKDOWN_INSTANCE = MarkdownRenderer()


# Templating configuration

TEMPLATE_NAME: str = "blogtastic"  # You can try "alt" or "default" here as well

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
        self.template_config = (
            yaml.safe_load(stream=open(TEMPLATE_DIR / "config.yml"))
            if os.path.exists(TEMPLATE_DIR / "config.yml")
            else {}
        )

    def render(
        self,
        location: str,
        context: Optional[Dict] = {},
        verbose: Optional[bool] = False,
    ) -> str:
        required_template = self.environment.get_template(location)
        return required_template.render(**context, **self.template_config)


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
