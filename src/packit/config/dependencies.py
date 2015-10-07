import os
from itertools import chain
from contextlib import contextmanager
from collections import deque, namedtuple

from pbr import packaging

from .base import BaseConfig


Requirements = namedtuple('Requirements', 'packages files links')


class DependenciesConfig(BaseConfig):
    requirements_base = [
        'requires',
        'requirements',
        'requirements/prod',
        'requirements/release',
        'requirements/install',
        'requirements/main',
        'requirements/base',
        ]

    requirements_test = [
        'test-requires',
        'test_requires',
        'test-requirements',
        'test_requirements',
        'requirements_test',
        'requirements-test',
        'requirements/test',
        'requirements/tests',
        ]

    requirements_extensions = [
        '',
        '.pip',
        '.txt',
        ]

    FIELD_INSTALL_REQUIRES = 'install'
    FIELD_TEST_REQUIRES = 'test'

    def __call__(self, config, facility_section_name):
        metadata = config.setdefault('metadata', {})
        backwards_compat = config.setdefault('backwards_compat', {})

        dependencies_facility_config = config.setdefault(facility_section_name, {})

        install = self._process_requirements(
            dependencies_facility_config, self.FIELD_INSTALL_REQUIRES, self.requirements_base
        )
        packaging.append_text_list(metadata, 'requires_dist', install.packages)

        test = self._process_requirements(
            dependencies_facility_config, self.FIELD_TEST_REQUIRES, self.requirements_test
        )
        packaging.append_text_list(backwards_compat, 'tests_require', test.packages)

        links = self._union(install.links, test.links)
        packaging.append_text_list(backwards_compat, 'dependency_links', links)

        referenced_files = self._union(install.files, test.files)
        files_config = config.setdefault('files', {})
        packaging.append_text_list(files_config, 'extra_files', referenced_files)

    @staticmethod
    def _union(*iterables):
        return sorted(set(chain.from_iterable(iterables)))

    @classmethod
    def _process_requirements(cls, config, field, defaults):
        existing_requirements_files = cls._get_requirements(config, field, defaults)
        top_one = existing_requirements_files[0] if existing_requirements_files else None

        if not top_one:
            return Requirements([], [], [])

        with cls._cd_to_file(top_one) as (dirname, filename):  # # pbr doesn't guess cwd from file path
            requirements = packaging.parse_requirements([filename])

        referenced_files = cls._find_linked_requirements_files(top_one)
        currdir = os.getcwd()
        normalized_referenced_files = [x[len(currdir) + 1:] for x in referenced_files]
        dependency_links = packaging.parse_dependency_links(referenced_files)

        return Requirements(requirements, normalized_referenced_files, dependency_links)

    @classmethod
    def _get_requirements(cls, config, field, lookup_files):
        requirements_file = config.get(field)

        if requirements_file:
            return [requirements_file]

        all_possible_options = cls._combine(lookup_files, cls.requirements_extensions)
        existing_files = filter(cls._is_file_exists, all_possible_options)
        return list(existing_files)

    @staticmethod
    def _combine(files, extensions):
        for filename in files:
            normalized_path = os.path.join(*filename.split('/'))  # in setup.cfg we expect / on any platform
            for ext in extensions:
                yield normalized_path + ext

    @staticmethod
    def _is_file_exists(path):
        return os.path.exists(path) and os.path.isfile(path)

    @classmethod
    def _find_linked_requirements_files(cls, *entry_files):
        result = set(map(os.path.abspath, entry_files))

        queue = deque(result)
        while queue:
            linked_files = cls._get_linked_files(queue.popleft())
            for filename in linked_files:
                if filename not in result:
                    result.add(filename)
                    queue.append(filename)

        return result

    @classmethod
    def _get_linked_files(cls, path):
        with cls._cd_to_file(path) as (dirname, filename):
            with open(filename) as f:
                lines = [l.strip() for l in f.readlines()]

            referenced_files = [l.partition(' ')[2] for l in lines if l.lower().startswith('-r')]
            return set(os.path.abspath(os.path.join(dirname, rfname)) for rfname in referenced_files)

    @staticmethod
    @contextmanager
    def _cd_to_file(filepath):
        currdir = os.getcwd()

        base, filename = os.path.split(filepath)
        dirname = base or currdir

        os.chdir(dirname)
        try:
            yield (dirname, filename)
        finally:
            os.chdir(currdir)


dependencies_config = DependenciesConfig()
