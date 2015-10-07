import os
from distutils import log
from collections import OrderedDict
from pkg_resources import to_filename

import glob2 as glob2

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
        self._expand_data_files_globs(files_config)
        self._expand_scripts_globs(files_config)
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

        resolved_files = []
        for pattern in filter(None, extra_files):
            for filename in self._expand_glob(pattern):
                self._add_file(filename)
                resolved_files.append(filename)

        files_config['extra_files'] = '\n'.join(resolved_files)

    @staticmethod
    def _get_packages_root(files_config):
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

    @staticmethod
    def _get_egg_info(metadata_config, packages_root):
        egg_name = metadata_config['name']
        egg_base = packages_root

        egg_info = to_filename(egg_name) + '.egg-info'
        if egg_base != os.curdir:
            egg_info = os.path.join(egg_base, egg_info)

        return egg_info

    def _expand_data_files_globs(self, files_config):
        data_files_str = files_config.get('data_files', '')

        if not data_files_str:
            return data_files_str

        data_files_lines = data_files_str.strip().split('\n')
        expanded_data_files = OrderedDict()  # expanded

        for line in data_files_lines:
            destination, sep, source = [x.strip() for x in line.partition('=')]

            real_source = source
            real_destination = destination

            expanded = []
            if source:
                # single line expression
                expanded = self._expand_glob(real_source)
            else:
                if sep:
                    # 1st line of multi-lin expression
                    real_destination = destination
                else:
                    real_source = destination
                    expanded = self._expand_glob(real_source)  # destination is actually source here

            for path in expanded:
                prefix = os.path.commonprefix([real_source, path])
                sub_path = path[len(prefix):]

                dirs, filename = os.path.split(sub_path)

                computed_destination = '/'.join(filter(None, [real_destination, dirs]))
                expanded_data_files.setdefault(computed_destination, []).append(path)

        referenced_files = []
        new_data_files_lines = []
        for destination, source in expanded_data_files.items():
            if not source:
                continue  # expanded to none

            if len(source) == 1:
                source_str = source[0]
                referenced_files.append(source_str)
            else:
                referenced_files.extend(source)
                source_str = '\n{}'.format('\n'.join(source))

            new_data_files_lines.append('{} = {}'.format(destination, source_str))

        new_data_files_str = '\n'.join(new_data_files_lines)
        files_config['data_files'] = new_data_files_str

        for fname in referenced_files:
            self._add_file(fname)

    @staticmethod
    def _expand_glob(pattern):
        expanded = glob2.iglob(pattern)
        return filter(os.path.isfile, expanded)

    def _expand_scripts_globs(self, files_config):
        scripts_str = files_config.get('scripts', '')
        scripts = filter(None, scripts_str.split('\n'))

        expanded_scripts = []
        for pattern in scripts:
            for filename in self._expand_glob(pattern):
                self._add_file(filename)
                expanded_scripts.append(filename)

        files_config['scripts'] = '\n'.join(expanded_scripts)


def git_files_finder():
    if not _get_git_directory():
        raise RuntimeError

    return _find_git_files()

extra_files_config = ExtraFilesConfig(additional_files, git_files_finder)
