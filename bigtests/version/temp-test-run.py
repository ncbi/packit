import wrap.config.version as v
import os.path
try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    from configparser import ConfigParser

config = ConfigParser()
config.read('setup.cfg')
config = dict(config._sections)

#config = {'auto-version': {'type': 'git-pep440'}, 'metadata': {'name': 'test-pkg'}}
v.version_config(config, 'auto-version')

import pprint
pprint.pprint(config)
