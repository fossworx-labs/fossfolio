from markdown import Markdown
import yaml
from typing import Optional, Any, Dict, List
from rich import print as rich_print
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

def run(template_str: str, *args, **kwargs) -> str:
    markdown_render = Markdown(extensions=['meta'])
    
    modified_str: str = markdown_render.convert(template_str)
    meta: Dict[str, Any] = markdown_render.Meta.copy()
    # rich_print(meta)
    if "draft" in meta and meta["draft"][0].lower() == "true":
        config = yaml.safe_load(open(CURRENT_DIR.absolute() / "config.yml", "r").read())
        # rich_print(config)
        template_string: str = config["template_string"]
        template_str = str(template_string)
    return template_str

if __name__ == "__main__":
    run("Hello there!")