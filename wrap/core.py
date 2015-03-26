from __future__ import print_function


def wrap(dist, attr, value):
    import pbr.hooks

    from .hooks import setup_hook
    pbr.hooks.setup_hook = setup_hook

    from pbr.core import pbr

    pbr(dist, attr, value)


def list_files(dir_name):
    return []
