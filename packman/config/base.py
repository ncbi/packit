class BaseConfig(object):

    def __call__(self, config, facility_section_name):
        raise NotImplementedError
