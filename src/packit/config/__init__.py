from collections import OrderedDict

from packit.utils import parse_boolean

from .version import version_config
from .packages import packages_config
from .auto_tests import auto_tests_config
from .extra_files import extra_files_config
from .dependencies import dependencies_config
from .description import auto_description_config
from .license import auto_license_config
from .extra_meta import extra_meta_config


class PackitFacilities(object):

    def __init__(self, config_section_name):
        self._default = set()
        self._registry = OrderedDict()
        self._config_section_name = config_section_name

    def add_facility(self, name, target, default=False):
        self._registry[name] = target
        if default:
            self._default.add(name)

    def get_enabled_facilities(self, config):
        facilities_section = config.get(self._config_section_name, {})

        enabled_facilities = set()
        for facility_name in self._registry:
            is_enabled = None

            # if facility explicitly disabled in facilities config then we force it off
            if facilities_section:
                is_enabled = self._is_facility_enabled(facilities_section, facility_name)

            if is_enabled is None:  # facility config not provided
                # check whether facility config section present or facility is enabled by default
                is_enabled = facility_name in config or facility_name in self._default

            if is_enabled:
                enabled_facilities.add(facility_name)

        # TODO: check for unrecognized sections and/or facilities

        return OrderedDict((k, v) for k, v in self._registry.items() if k in enabled_facilities)

    @staticmethod
    def _is_facility_enabled(option_dict, option_name):
        """
        :return: True if explicitly enabled, False if explicitly disabled, None if no value provided
        """
        if option_name not in option_dict:
            return

        return parse_boolean(option_dict[option_name])

packit_facilities = PackitFacilities('facilities')


packit_facilities.add_facility('auto-version', version_config, default=True)
packit_facilities.add_facility('auto-description', auto_description_config, default=True)
packit_facilities.add_facility('auto-license', auto_license_config, default=True)
packit_facilities.add_facility('auto-dependencies', dependencies_config, default=True)
packit_facilities.add_facility('auto-packages', packages_config, default=True)
packit_facilities.add_facility('auto-package-data', extra_files_config, default=True)
packit_facilities.add_facility('auto-tests', auto_tests_config, default=True)
packit_facilities.add_facility('auto-extra-meta', extra_meta_config, default=True)
