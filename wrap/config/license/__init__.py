import os

from wrap.config.base import BaseConfig


class LicenseConfig(BaseConfig):
    def __call__(self, config, facility_section_name):
        config['metadata']['license-file'] = os.path.join(os.path.dirname(__file__), 'NCBI_LICENSE')


license_config = LicenseConfig()