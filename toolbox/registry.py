__author__ = 'jeff'
from .plugin import ToolboxPlugin
from .mixins import RegistryMixin
import importlib

class NoPluginException (Exception):
    pass

class Registry(object):
    """
    Registry of all available plugins
    """
    _registered_plugins = {}

    def add_plugin(self, plugin):
        """
        Add a ToolboxPlugin to the registry.
         Instances of toolbox plugins need a name attribute for this to work

        :param plugin:
        :return:
        """
        if not isinstance(plugin , ToolboxPlugin):
            raise NoPluginException('provided plugin argument is not does not extend the core ToolboxPlugin class')
        if not hasattr(plugin, 'name') or plugin.name is None:
            raise AttributeError('Plugin has no name attribute set')
        if not hasattr(plugin, 'description') or plugin.description is None:
            raise AttributeError("Plugin {} has no description".format(plugin.description))

        if isinstance(plugin, RegistryMixin):
            plugin.set_registry(self)

        self._registered_plugins[plugin.name] = plugin


    def populate(self, modules):
        """
        Given a list of 'importable' modules populate the registry
        :param modules:
        :return:
        """
        for module in modules:
            m = importlib.import_module(module)

            if not hasattr(m,'Plugin'):
                raise NoPluginException('Module: {} has no plugin set'.format(module))

            self.add_plugin(m.Plugin)

    def get_plugin_names(self):
        return self._registered_plugins.keys()


    def get_plugins(self):
        """
        :return: List of registered plugins
        :rtype: list
        """
        return self._registered_plugins.values()

    def get_plugin(self,name):
        if name in self._registered_plugins:
            return self._registered_plugins[name]

        raise ValueError('the {} Plugin is not registered'.format(name))
