import os
import codecs
from distutils import log

from packit.utils import get_version_from_meta
from packit.config.base import BaseConfig

from .file import file_version_generator
from .fixed import fixed_version_generator
from .git_pep440 import git_pep440_version_generator
from .composite import composite_version_generator
from .shell import shell_version_generator


class VersionConfig(BaseConfig):
    FIELD_VERSION_STRATEGY = 'type'
    FIELD_VERSION_VALUE = 'value'
    FIELD_OUTPUT = 'output'

    def __init__(self):
        self._registry = {}
        self._default_version_strategy = None

    def __call__(self, config, facility_section_name):
        """
        :param dict config:
        """

        version = get_version_from_meta(config['metadata']['name'])

        if not version:
            version = self._resolve_package_version(config, facility_section_name)

        if not version:
            raise ValueError('Cannot find any version number!')

        config['metadata']['version'] = version

    def _resolve_package_version(self, config, facility_section_name):
        base_version_config, extra_version_config = self._get_facility_config(config, facility_section_name)

        sub_versions = {}
        if extra_version_config:
            for sub_key, sub_config in extra_version_config.items():
                sub_versions[sub_key] = self._process_version_config(sub_key, sub_config, kwargs=sub_versions)

        return self._process_version_config(facility_section_name, base_version_config, self._default_version_strategy,
                                            sub_versions)

    def _process_version_config(self, name, strategy_config, default_strategy=None, kwargs=None):
        try:
            version_type = strategy_config[self.FIELD_VERSION_STRATEGY]
        except KeyError:
            if default_strategy:
                version_type = default_strategy
            else:
                raise ValueError('No default version strategy :(')

        version_value = strategy_config.get(self.FIELD_VERSION_VALUE)

        try:
            version_strategy = self._registry[version_type]
        except KeyError:
            raise ValueError('Oh no! Unknown version strategy!')

        resolved_version = version_strategy(version_value, **(kwargs or {}))

        output_filename = strategy_config.get(self.FIELD_OUTPUT)
        if output_filename:
            norm_filename = os.path.join(*output_filename.split('/'))
            try:
                with codecs.open(norm_filename, mode='w', encoding='utf-8') as fp:
                    fp.write(resolved_version)
            except IOError:
                log.fatal("[{facility}] Cannot write version to {fn}".format(
                    facility=name, fn=norm_filename
                ))
                raise SystemExit(1)

        # TODO: deal gracefully with failed attempts, with a nice error message.
        # (e.g. no git binary, file doesn't exist, etc)
        return resolved_version

    def add_version_strategy(self, name, strategy, default=False):
        self._registry[name] = strategy
        if default:
            self._default_version_strategy = name


version_config = VersionConfig()

version_config.add_version_strategy('file', file_version_generator)
version_config.add_version_strategy('fixed', fixed_version_generator)
version_config.add_version_strategy('git-pep440', git_pep440_version_generator, default=True)
version_config.add_version_strategy('shell', shell_version_generator)
version_config.add_version_strategy('composite', composite_version_generator)
