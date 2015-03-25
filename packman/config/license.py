from .base import BaseConfig


class LicenseConfig(BaseConfig):
    def __call__(self, config, facility_section_name):
        raise NotImplementedError


license_config = LicenseConfig()