from pbr import hooks, pbr_json
from pbr.core import pbr

from .hooks import setup_hook


def packit(dist, attr, value):
    if not value:
        return

    hooks.setup_hook = setup_hook
    # Disabling annoying pbr.json
    pbr_json.write_pbr_json = lambda *a, **k: None

    pbr(dist, attr, value)
