import os

from itertools import product

from pbr import packaging

from .base import BaseConfig


class AutoDescriptionConfig(BaseConfig):
    FIELD_DESCRIPTION = 'description'

    FIELD_FILE = 'file'

    KNOWN_FILENAMES = [
        'README',
        'readme',
        'CHANGELOG',
        'changelog',
    ]

    KNOWN_EXTENSIONS = [
        '',
        '.md', '.markdown', '.mkdn', '.text',
        '.rst',
        '.txt',
    ]

    def __call__(self, config, facility_section_name):
        metadata_config = config.setdefault('metadata', {})

        if self.FIELD_DESCRIPTION in metadata_config:
            return

        description_config = config.setdefault(facility_section_name, {})
        filename = description_config.get(self.FIELD_FILE)

        if not filename:
            filename = self._find_readme_file('.')

        if not filename:
            return

        metadata_config[self.FIELD_DESCRIPTION] = self._read_file(filename)

        files_config = config.setdefault('files', {})
        packaging.append_text_list(files_config, 'extra_files', [filename])

    def _find_readme_file(self, target_dir):
        for filename, extension in product(self.KNOWN_FILENAMES, self.KNOWN_EXTENSIONS):
            path = os.path.join(target_dir, filename + extension)
            if os.path.exists(path) and os.path.isfile(path):
                return path

    def _read_file(self, filename):
        with open(filename) as f:
            return f.read()


auto_description_config = AutoDescriptionConfig()
