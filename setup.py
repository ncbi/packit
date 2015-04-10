from setuptools import setup
from setuptools.dist import Distribution


class PacKitDist(Distribution):
    def __init__(self, attrs=None):
        self._packit_inited = False
        Distribution.__init__(self, attrs)

    def fetch_build_eggs(self, requires):
        Distribution.fetch_build_eggs(self, requires)

        if not self._packit_inited:
            import sys
            if 'src' not in sys.path:
                sys.path.insert(0, 'src')

            try:
                from packit.core import patch_pbr
                patch_pbr()
            except ImportError:
                pass
            else:
                self._packit_inited = True


setup(distclass=PacKitDist, setup_requires=['pbr'], pbr=True)
