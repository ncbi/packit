from pbr import packaging

from .base import BaseConfig


class AutoTestsConfig(BaseConfig):
    requirements = [
        'tox>=1.9.2',
        'pytest>=2.7.0',
        'pytest-cov>=1.8.1',
        'pytest-xdist>=1.11',
        'coverage>=3.7.1,<4',
        'teamcity-messages>=1.12',
    ]

    def __call__(self, config, facility_section_name):
        global_config = config.setdefault('global', {})
        current_commands = global_config.get('commands', '')
        global_config['commands'] = '\n'.join(['packman.commands.packman_test.PackmanTest', current_commands])

        backwards_compat_config = config.setdefault('backwards_compat', {})
        packaging.append_text_list(backwards_compat_config, 'tests_require', self.requirements)

auto_tests_config = AutoTestsConfig()
