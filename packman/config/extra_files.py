import os

from pbr.git import _find_git_files

from packman_extra.additional_files import additional_files
from .base import BaseConfig


class ExtraFilesConfig(BaseConfig):

    def __call__(self, config, facility_section_name):
        files_config = config.setdefault('files', {})

        packages = files_config.get('packages', '').strip()
        if not packages:
            return

        package_list = packages.split('\n')

        root = files_config.get('packages_root', '')
        all_git_files = _find_git_files()
        extra_files_in_root = [f for f in all_git_files if f.startswith(root) and not f.endswith('.py')]

        package_paths = [os.path.join(root, *p.split('.')) for p in package_list]

        for filename in extra_files_in_root:
            if any(filename.startswith(p) for p in package_paths):
                additional_files.add(filename)

extra_files_config = ExtraFilesConfig()
