__author__ = 'jeff'


class RegistryMixin(object):
    """
    The RegistryMixin provides the plugin with an registry interface.
    Plugins that subclass this mixin get full access to the toolbox registry so you could use plugins within plugins
    """
    _registry = None

    def set_registry(self, registry):
        self._registry = registry

    def get_registry(self):
        return self._registry


class ConfigMixin(object):
    """
    The ConfigMixin provides the plugin with an persisted py:class:`toolbox.config.PluginConfig` which is basically an
    expanded python dictionary which contains the plugin config as well as an global config.
    """

    def set_config(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def get_global_config(self):
        return self.get_config().get_global_config()


class LogMixin(object):
    """
    The LogMixin provides the plugin with a zero configuration python logger.
    """
    _logger = None

    def set_logger(self, logger):
        self._logger = logger

    def get_logger(self):
        return self._logger
