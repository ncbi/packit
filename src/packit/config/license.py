import os

from itertools import product

from pbr import packaging

from .base import BaseConfig


class AutoLicenseConfig(BaseConfig):
    FIELD_LICENSE_FILE = 'file'

    KNOWN_FILENAMES = [
        'LICENSE',
        'license',
    ]

    KNOWN_EXTENSIONS = [
        '',
        '.md', '.markdown', '.mkdn', '.text',
        '.rst',
        '.txt',
    ]

    def __call__(self, config, facility_section_name):
        license_config = config.setdefault(facility_section_name, {})

        license_file = license_config.get(self.FIELD_LICENSE_FILE)
        if not license_file:
            license_file = self._find_license_file('.')

        if not license_file:
            return

        files_config = config.setdefault('files', {})
        packaging.append_text_list(files_config, 'extra_files', [license_file])

    def _find_license_file(self, target_dir):
        for filename, extension in product(self.KNOWN_FILENAMES, self.KNOWN_EXTENSIONS):
            path = os.path.join(target_dir, filename + extension)
            if os.path.exists(path) and os.path.isfile(path):
                return path


auto_license_config = AutoLicenseConfig()
