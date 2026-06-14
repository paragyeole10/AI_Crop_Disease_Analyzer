import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    """
    Load settings from the central config.yaml file.
    """
    config_path = os.path.join(BASE_DIR, "config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def get_absolute_path(relative_path):
    """
    Resolve a relative path from the config into an absolute path based on project root.
    """
    if not relative_path:
        return ""
    if os.path.isabs(relative_path):
        return relative_path
    return os.path.normpath(os.path.join(BASE_DIR, relative_path))
