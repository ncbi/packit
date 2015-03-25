class Registry(object):
    DEFAULT_FACTORY = staticmethod(lambda name, target: target)

    def __init__(self, factory=DEFAULT_FACTORY):
        self._registry = {}
        self._factory = factory

    def __call__(self, name):
        def appender(target):
            self._registry[name] = self._factory(name, target)

        return appender

    def get_facilities(self):
        return self._registry.copy()
