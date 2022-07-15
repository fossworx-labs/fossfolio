from markdown import Markdown
import yaml
from typing import Optional, Any, Dict, List
from rich import print as rich_print
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

def run(template_dict: dict, verbose: Optional[bool] = False, *args, **kwargs) -> str:
    markdown_render = Markdown(extensions=['meta'])
    
    if verbose:
        rich_print(f"[bold red]{__file__} > run[/bold red] Received template dict: {template_dict}")
    modified_str: str = markdown_render.convert(template_dict["content"])
    meta: Dict[str, Any] = markdown_render.Meta.copy()
    # rich_print(meta)
    if "draft" in meta and meta["draft"][0].lower() == "true":
        config = yaml.safe_load(open(CURRENT_DIR.absolute() / "config.yml", "r").read())
        # rich_print(config)
        template_string: str = config["template_string"]
        template_dict["content"] = str(template_string)
    return template_dict

if __name__ == "__main__":
    run("Hello there!")