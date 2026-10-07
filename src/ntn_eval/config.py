"""Configuration loading for ntn-eval.

All simulation parameters live in YAML files under configs/. This module
loads them into plain dicts with a small helper for nested access.
"""
import os
import yaml

CONFIG_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "configs"))


def load(name):
    """Load configs/<name>.yaml and return the parsed dict."""
    path = os.path.join(CONFIG_DIR, name + ".yaml")
    with open(path) as f:
        return yaml.safe_load(f)


def load_all():
    """Load every config file used by the evaluation."""
    return {
        "modes": load("modes"),
        "agri": load("agri"),
        "env": load("env"),
        "ntn": load("ntn"),
        "energy": load("energy"),
    }
