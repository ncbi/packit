import os

from itertools import chain
from collections import deque

from pbr import packaging

from .base import BaseConfig


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

        install_requirements = self._get_requirements(dependencies_facility_config, self.FIELD_INSTALL_REQUIRES,
                                                      self.requirements_base)

        test_requirements = self._get_requirements(dependencies_facility_config, self.FIELD_TEST_REQUIRES,
                                                   self.requirements_test)

        packaging.append_text_list(metadata, 'requires_dist', packaging.parse_requirements(install_requirements))
        packaging.append_text_list(backwards_compat, 'tests_require', packaging.parse_requirements(test_requirements))

        base_links = packaging.parse_dependency_links(install_requirements)
        test_links = packaging.parse_dependency_links(test_requirements)

        links = list(set(base_links + test_links))
        packaging.append_text_list(backwards_compat, 'dependency_links', links)

        referenced_files = self._find_linked_requirements_files(chain(install_requirements, test_requirements))
        files_config = config.setdefault('files', {})
        packaging.append_text_list(files_config, 'extra_files', referenced_files)

    @staticmethod
    def _combine(files, extensions):
        for filename in files:
            normalized_path = os.path.join(*filename.split('/'))
            for ext in extensions:
                yield normalized_path + ext

    @staticmethod
    def _is_file_exists(path):
        return os.path.exists(path) and os.path.isfile(path)

    def _get_requirements(self, config, field, lookup_files):
        requirements = config.get(field)

        if requirements:
            return [requirements]

        return list(filter(self._is_file_exists, self._combine(lookup_files, self.requirements_extensions)))

    def _find_linked_requirements_files(self, entry_files):
        result = set(entry_files)

        queue = deque(entry_files)
        while queue:
            linked_files = self._get_linked_files(queue.popleft())
            for filename in linked_files:
                if filename not in result:
                    result.add(filename)
                    queue.append(filename)

        return result

    def _get_linked_files(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        return set(l.partition(' ')[2] for l in lines if l.startswith('-r'))


dependencies_config = DependenciesConfig()
