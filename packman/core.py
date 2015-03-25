from pbr.core import pbr
from pbr.util import cfg_to_args


def packman(dist, attr, value):
    pbr(dist, attr, value)


def setup_kwargs():
    return cfg_to_args()