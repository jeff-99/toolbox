__author__ = 'jeff'

class RegistryMixin(object):

    _registry = None

    def set_registry(self, registry):
        self._registry = registry

    def get_registry(self):
        return self._registry