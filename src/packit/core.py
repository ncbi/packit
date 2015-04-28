from pbr import hooks, pbr_json
from pbr.core import pbr

from .hooks import setup_hook


def patch_pbr(config=None):
    hooks.setup_hook = setup_hook
    # Disabling annoying pbr.json
    pbr_json.write_pbr_json = lambda *a, **k: None


def packit(dist, attr, value):
    if not value:
        return

    patch_pbr()

    pbr(dist, attr, value)
