from pbr import hooks, util
from pbr.core import pbr

from .hooks import setup_hook


def _patch_pbr():
    hooks.setup_hook = setup_hook
    # Disabling annoying pbr.json
    pbr_json.write_pbr_json = lambda *a, **k: None


def packman(dist, attr, value):
    if value:
        _patch_pbr()

    pbr(dist, attr, value)

