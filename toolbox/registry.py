__author__ = 'jeff'
from .plugin import ToolboxPlugin
from .mixins import RegistryMixin, ConfigMixin
from .config import ConfigManager
import importlib, inspect

class NoPluginException (Exception):
    pass

class Registry(object):
    """
    Registry of all available plugins
    Setup the config manager and creates two empty dicts to track the tools

    :ivar `toolbox.config.ConfigManager` config_manager: Instance of the config manager
    :ivar dict _registered_plugins: dictionary containing all registered plugins
    :ivar dict _loaded_plugins: dictionary containing all fully loaded plugins

    """
    def __init__(self):
        self.config_manager = ConfigManager()
        self._registered_plugins = {}
        self._loaded_plugins = {}

    def add_plugin(self, plugin):
        """
        Add a :py:class:`toolbox.plugin.ToolboxPlugin` to the registry, but don't load it yet
         Checks whether the provided plugin is an instance of :py:class:`toolbox.plugin.ToolboxPlugin`

        :param plugin: A plugin to add to the registry
        :type plugin: :py:class:`toolbox.plugin.ToolboxPlugin`
        :raises: :py:class:`AtttibuteError`, :py:class:`toolbox.registry.NoPluginException`
        :return:
        """
        if not isinstance(plugin, ToolboxPlugin):
            raise NoPluginException('provided plugin argument is not does not extend the core ToolboxPlugin class')
        if not hasattr(plugin, 'name') or plugin.name is None:
            raise AttributeError('Plugin has no name attribute set')
        if not hasattr(plugin, 'description') or plugin.description is None:
            raise AttributeError("Plugin {} has no description".format(plugin.description))

        self._registered_plugins[plugin.name] = plugin

    def _load_plugin(self, plugin):
        if isinstance(plugin, RegistryMixin):
            plugin.set_registry(self)

        if isinstance(plugin, ConfigMixin):
            config = self.config_manager.load_plugin(plugin.name)
            plugin.set_config(config)

        return plugin


    def populate(self, modules):
        """
        Given a list of 'importable' modules populate the registry
        First import the module, check whether it has a 'Plugin' attribute in the namespace and
        add the plugin to the registry

        Also accepts an module where there is a class definition suffixed by 'Plugin' like 'TestPlugin'

        :param list modules:
        :return:
        """
        for module in modules:
            m = importlib.import_module(module)

            if hasattr(m,'Plugin'):
                self.add_plugin(m.Plugin)
                continue

            for name, plugin_class in inspect.getmembers(m):
                if 'Plugin' in name:
                    p = plugin_class()
                    self.add_plugin(p)



    def get_plugin_names(self):
        """
        :return: the list of registered plugins (names)
        :rtype: list
        """
        return self._registered_plugins.keys()

    def get_plugins(self):
        """
        :return: List of registered plugins
        :rtype: list
        """
        return self._registered_plugins.values()

    def get_plugin(self,name):
        """
        fetch a plugin from the registry and load it if it is not loaded already.

        :param str name: Name of the registered plugin
        :return: An loaded plugin
        :rtype: :py:class:`toolbox.plugin.ToolboxPlugin`
        :raise: :py:class:`ValueError`
        """
        if name in self._loaded_plugins:
            return self._loaded_plugins[name]

        if name in self._registered_plugins:
            plugin = self._load_plugin(self._registered_plugins[name])
            self._loaded_plugins[name] = plugin
            return plugin

        raise ValueError('the {} Plugin is not registered'.format(name))

    def shutdown(self):
        """
        Shutdown the registry and notify the config manager to shutdown
        :return:
        """
        self.config_manager.save(self._loaded_plugins.values())
