from pbr.core import pbr
from pbr import pbr_json


def packman(dist, attr, value):
    if value:
        pbr_json.write_pbr_json = lambda *a, **k: None

    pbr(dist, attr, value)
