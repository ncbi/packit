from distutils import log
from collections import OrderedDict


class BaseConfig(object):

    def __call__(self, config, facility_section_name):
        raise NotImplementedError

    @staticmethod
    def _get_facility_config(config, facility_section_name, separator=':'):
        facility_config = config.setdefault(facility_section_name, {})

        extra_config = OrderedDict()
        for key in config:
            if separator not in key:
                continue

            tokens = key.split(separator, 1)
            main_token, extra_name = tokens
            if main_token != facility_section_name:
                continue

            if not extra_name:
                log.fatal("[{facility}] The '{key}' is wrong section name (it cannot end with a colon)".format(
                    facility=facility_section_name, key=key
                ))
                raise SystemExit(1)

            extra_config[extra_name] = config[key]

        return facility_config, extra_config
