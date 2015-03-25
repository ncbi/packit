from pbr import packaging

from packman.config.base import BaseConfig


class MetadataConfig(BaseConfig):

    section = 'metadata'

    def hook(self):
        packaging.append_text_list(self.config, 'requires_dist', packaging.parse_requirements())

    def get_name(self):
        return self.config['name']