__author__ = 'jeff'

class RegistryMixin(object):


    _registry = None

    def set_registry(self, registry):
        self._registry = registry

    def get_registry(self):
        return self._registry


class ConfigMixin(object):
    def set_config(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def get_global_config(self):
        return self.get_config().get_global_config()


class LogMixin(object):
    _logger = None

    def set_logger(self, logger):
        self._logger = logger

    def get_logger(self):
        return self._logger