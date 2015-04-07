import packit.config.version as v

try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    from configparser import ConfigParser

config = ConfigParser()
config.read('setup.cfg')
config = dict(config._sections)


v.version_config(config, 'auto-version')

import pprint
pprint.pprint(config)
