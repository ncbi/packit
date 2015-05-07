import os
from fnmatch import fnmatch

from setuptools import find_packages

from .base import BaseConfig


class PackageConfig(BaseConfig):

    def __init__(self, default_include=(), default_exclude=('test*', 'docs', '.tox', 'env')):
        self._default_include = default_include
        self._default_exclude = default_exclude

    def __call__(self, config, facility_section_name):
        self_config = config.get(facility_section_name, {})
        files_config = config.setdefault('files', {})

        root = files_config.get('packages_root', '')
        packages = files_config.get('packages', '').strip()

        if packages:
            return

        exclude = self._get_list_option(self_config, 'exclude') or self._default_exclude or ()
        include = self._get_list_option(self_config, 'include') or self._default_include or ()

        found_packages = set()

        if not include:
            if root:
                include = [root]
            else:
                include = self._smart_default_include(exclude)
                found_packages |= include

        for path in include:
            found_packages |= set(find_packages(path, exclude))

        files_config['packages'] = "\n".join(found_packages)

    def _smart_default_include(self, exclude):
        root_dirs = filter(os.path.isdir, os.listdir('.'))
        root_packages = {name for name in root_dirs if os.path.exists(os.path.join(name, '__init__.py'))}
        return {path for path in root_packages if not any(fnmatch(path, pattern) for pattern in exclude)}

    def _get_list_option(self, cfg, key):
        return set(filter(None, cfg.get(key, '').strip().split('\n')))

packages_config = PackageConfig()