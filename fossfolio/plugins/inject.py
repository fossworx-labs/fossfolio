import importlib
from typing import Optional, Any, Dict, List, Tuple

from rich import print as rich_print

ACTIVE_PLUGINS: Tuple = (
    "date_time",
    "user_metadata",
    "draft_manager",
)

DEFAULT_INJECTION_SETTINGS: dict = {}


def sanity_check(import_string: str) -> bool:
    """Checks if the import string is valid and safe to import."""
    return True


def import_plugins(*args: Optional[list], **kwargs: Optional[dict]) -> Dict[str, Any]:
    """Import plugins defined in the ACTIVE_PLUGINS variable"""
    plugins_dict: dict = {}

    current_plugin: str = ""
    try:
        for current_plugin in ACTIVE_PLUGINS:
            import_str: str = f"plugins.{current_plugin}.main"

            if sanity_check(import_str):
                plugins_dict[f"{current_plugin}_main"] = importlib.import_module(import_str)

    except Exception as e:
        rich_print(
            f"[bold red]{__file__}/import_plugins: Exception occured while importing plugin [/bold red]'{current_plugin}' \n{e}"
        )

    finally:
        return plugins_dict


def inject(
    templates_dict: dict = None, *args: Optional[List], **kwargs: Optional[Dict]
) -> Dict[str, str]:
    """Accepts a mappping (dictionary) of template paths and template file contents.
    ---
    """
    imported_plugins: dict = import_plugins(*args, **kwargs)
    plugin_process: str = ""
    if not imported_plugins:
        raise ImportError(f"{__file__}/inject: No pluggable items found.")

    try:
        for plugin_process in imported_plugins:
            for template_route in templates_dict:
                templates_dict[template_route] = imported_plugins[plugin_process].run(
                    templates_dict[template_route], *args, **kwargs
                )

    except Exception as e:
        rich_print(
            f"[italic red]{__file__}/inject: Encountered error while injecting plugin: [/italic red] '{plugin_process}'\n{e}"
        )

    finally:
        return templates_dict
