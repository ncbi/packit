from ..base import BaseConfig

import pbr.packaging

from .file import file_version_generator
from .fixed import fixed_version_generator
from .git_pep440 import git_pep440_version_generator
from .shell import shell_version_generator


class VersionConfig(BaseConfig):
    FIELD_VERSION_STRATEGY = 'type'
    FIELD_VERSION_VALUE = 'value'

    def __init__(self):
        self._registry = {}
        self._default_version_strategy = None

    def __call__(self, config, facility_section_name):
        """
        :param dict config:
        """

        version = pbr.packaging._get_version_from_pkg_info(
            config['metadata']['name'])

        if not version:
            version = self._get_version_using_strategy(
                config,
                facility_section_name)

        if not version:
            raise ValueError('Cannot find any version number!')

        config['metadata']['version'] = version

    def _get_version_using_strategy(self, config, facility_section_name):
        version_config_section = config.get(facility_section_name, {})

        try:
            version_type = version_config_section[self.FIELD_VERSION_STRATEGY]
        except KeyError:
            if self._default_version_strategy:
                version_type = self._default_version_strategy
            else:
                raise ValueError('No default version strategy :(')

        version_value = version_config_section.get(self.FIELD_VERSION_VALUE)

        try:
            version_strategy = self._registry[version_type]
        except KeyError:
            raise ValueError('Oh no! Unknown version strategy!')

        # TODO: deal gracefully with failed attempts, with a nice error message.
        # (e.g. no git binary, file doesn't exist, etc)
        return version_strategy(version_value)

    def add_version_strategy(self, name, strategy, default=False):
        self._registry[name] = strategy
        if default:
            self._default_version_strategy = name


version_config = VersionConfig()

version_config.add_version_strategy('file', file_version_generator)
version_config.add_version_strategy('fixed', fixed_version_generator)
version_config.add_version_strategy('git-pep440', git_pep440_version_generator, default=True)
version_config.add_version_strategy('shell', shell_version_generator)
