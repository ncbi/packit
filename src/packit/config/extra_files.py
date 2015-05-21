import os
from distutils import log

from pkg_resources import to_filename

from pbr.git import _find_git_files, _get_git_directory

from packit.additional_files import additional_files
from packit.utils import parse_boolean

from .base import BaseConfig


class ExtraFilesConfig(BaseConfig):
    FIELD_EVERYTHING = 'everything'

    def __init__(self, file_set, finder):
        self._file_set = file_set
        self._finder = finder

    def __call__(self, config, facility_section_name):
        metadata_config = config.setdefault('metadata', {})

        files_config = config.setdefault('files', {})
        self._add_extra_files_from_cfg(files_config)

        root = self._get_packages_root(files_config)

        try:
            external_extra_files = self._finder()
        except RuntimeError:
            # Looks like someone tries to install us
            external_extra_files = self._get_extra_files_from_egg_info(metadata_config, root)

        facility_config = config.setdefault(facility_section_name, {})
        if parse_boolean(facility_config.get(self.FIELD_EVERYTHING, '')):
            for filename in external_extra_files:
                self._add_file(filename)
                return  # TODO: refactor

        # TODO: add option to disable auto package-data

        packages = files_config.get('packages', '').strip()
        if not packages:
            return

        package_list = packages.split('\n')

        if root and not os.path.isdir(root):
            log.fatal("[%s] The 'packages_root' value should be a dir name" % facility_section_name)
            raise SystemExit(1)

        extra_files_in_root = [f for f in external_extra_files
                               if os.path.commonprefix([root, f]) == root and not f.endswith('.py')]

        package_paths = [os.path.join(root, *p.split('.')) for p in package_list]

        for filename in filter(None, extra_files_in_root):
            if any(filename.startswith(p) for p in package_paths):
                self._add_file(filename)

    def _add_extra_files_from_cfg(self, files_config):
        extra_files = files_config.get('extra_files', '').strip().split('\n')

        for filename in filter(None, extra_files):
            self._add_file(filename)

    def _get_packages_root(self, files_config):
        root = files_config.get('packages_root', '')

        if root == '.':
            root = ''
        return root

    def _add_file(self, filename):
        self._file_set.add(filename.strip())

    def _get_extra_files_from_egg_info(self, metadata_config, root):
        egg_info = self._get_egg_info(metadata_config, root)
        sources = os.path.join(egg_info, 'SOURCES.txt')

        result = []
        if os.path.isfile(sources):
            with open(sources) as f:
                result = f.read().split()

        return result

    def _get_egg_info(self, metadata_config, packages_root):
        egg_name = metadata_config['name']
        egg_base = packages_root

        egg_info = to_filename(egg_name) + '.egg-info'
        if egg_base != os.curdir:
            egg_info = os.path.join(egg_base, egg_info)

        return egg_info


def git_files_finder():
    if not _get_git_directory():
        raise RuntimeError

    return _find_git_files()

extra_files_config = ExtraFilesConfig(additional_files, git_files_finder)
