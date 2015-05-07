from .base import BaseConfig


class AutoTestsConfig(BaseConfig):

    def __call__(self, config, facility_section_name):
        global_config = config.setdefault('global', {})
        current_commands = global_config.get('commands', '')
        global_config['commands'] = '\n'.join(['packit.commands.packit_test.PackitTest', current_commands])

auto_tests_config = AutoTestsConfig()
