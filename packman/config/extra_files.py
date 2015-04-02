import os

from pbr.git import _find_git_files

from packman.additional_files import additional_files
from .base import BaseConfig


class ExtraFilesConfig(BaseConfig):

    def __init__(self, file_set, finder):
        self._file_set = file_set
        self._finder = finder

    def _add_extra_files(self, files_config):
        extra_files = files_config.get('extra_files', '').strip().split('\n')

        for filename in filter(None, extra_files):
            self._add_file(filename)

    def __call__(self, config, facility_section_name):
        files_config = config.setdefault('files', {})

        self._add_extra_files(files_config)

        # TODO: add option to disable auto package-data

        packages = files_config.get('packages', '').strip()
        if not packages:
            return

        package_list = packages.split('\n')

        root = files_config.get('packages_root', '')
        extra_files_in_root = [f for f in self._finder() if f.startswith(root) and not f.endswith('.py')]

        package_paths = [os.path.join(root, *p.split('.')) for p in package_list]

        for filename in filter(None, extra_files_in_root):
            if any(filename.startswith(p) for p in package_paths):
                self._add_file(filename)

    def _add_file(self, filename):
        self._file_set.add(filename.strip())

extra_files_config = ExtraFilesConfig(additional_files, _find_git_files)
