from setuptools import find_packages

from .base import BaseConfig


class PackageConfig(BaseConfig):

    def __init__(self, default_include=(), default_exclude=('test*', 'docs', '.tox', 'env')):
        self._default_include = default_include
        self._default_exclude = default_exclude

    def __call__(self, config, facility_section_name):
        files_config = config.setdefault('files', {})
        packages = files_config.get('packages', '').strip()

        if packages:
            return

        self_config = config.get(facility_section_name, {})
        exclude = self._get_list_option(self_config, 'exclude') or self._default_exclude or ()
        include = self._get_list_option(self_config, 'include') or self._default_include or ()

        include = include or [files_config.get('packages_root', '.')]

        found_packages = set()
        for path in include:
            found_packages |= set(find_packages(path, exclude))

        files_config['packages'] = "\n".join(found_packages)

    @staticmethod
    def _get_list_option(cfg, key):
        return set(filter(None, cfg.get(key, '').strip().split('\n')))

packages_config = PackageConfig()
