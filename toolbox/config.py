import json
import collections
from .mixins import ConfigMixin
from .defaults import *


class ConfigManager(object):
    """
    The config manager has the responsibility of persisting plugin configs.
    On initialisation it creates a default file structure in the user's home directory
    """
    FILE_EXT = '.json'

    def __init__(self):
        if not os.path.isdir(TOOLBOX_DIR):
            os.mkdir(TOOLBOX_DIR)

        if not os.path.isdir(CONF_DIR):
            os.mkdir(CONF_DIR)

        if not os.path.isdir(LOCAL_PLUGIN_DIR):
            os.mkdir(LOCAL_PLUGIN_DIR)

        self.config_dir = CONF_DIR

    def load_plugin(self, name):
        """
        Load the plugin config file by name and return an py:class:`toolbox.config.PluginConfig`

        :param str name:
        :return: an instance of PluginConfig for given plugin name
        :rtype: toolbox.config.PluginConfig
        """
        file_name = name + ConfigManager.FILE_EXT
        path = os.path.join(self.config_dir, file_name)

        if not os.path.exists(path):
            plugin_config = PluginConfig()
        elif os.path.exists(path) and not os.path.isfile(path):
            raise TypeError('{} is not a file'.format(path))
        else:
            with open(path, 'r') as f:
                try:
                    config = json.load(f)
                    plugin_config = PluginConfig.create_from_dict(config)

                except ValueError:
                    plugin_config = PluginConfig()

        return plugin_config

    def save_plugin(self, name, config):
        """
        save a plugin config by name
        before saving the global config key is deleted

        :param str name: Name of the plugin
        :param config: instance of an py:class:`toolbox.config.PluginConfig`
        :return:
        """
        file_name = name + ConfigManager.FILE_EXT
        path = os.path.join(self.config_dir, file_name)

        if os.path.exists(path) and not os.path.isfile(path):
            raise Exception('path exists but it ain\'t a file Brah')

        if PluginConfig.GLOBAL_KEY in config:
            del config[PluginConfig.GLOBAL_KEY]

        with open(path, 'w') as f:
            f.write(config.to_json())

    def save(self, plugins):
        """
        Convenience method to save a list of plugins. Only configs that have been modified since loading will be saved.
        :param iterable plugins: list of instances of base class py:class:`toolbox.plugin.ToolboxPlugin`
        :return:
        """
        for plugin in plugins:
            if isinstance(plugin, ConfigMixin):
                conf = plugin.get_config()
                if conf.modified:
                    self.save_plugin(plugin.name, conf)


class PluginConfig(object):
    """
    Config container for plugin configs. Acts like a dictionary with some extra convenience methods.
    The config has a special key for global configs which can be accessed with the 'get_global_config' method
    """
    GLOBAL_KEY = '__GLOBAL__'

    def __init__(self):
        self._config = collections.defaultdict(lambda: None)
        self.modified = False

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self.modified = True if key != PluginConfig.GLOBAL_KEY else False
        self._config[key] = value

    def __delitem__(self, key):
        self.modified = True if key != PluginConfig.GLOBAL_KEY else False
        del self._config[key]

    def __contains__(self, item):
        return item in self._config

    def __add__(self, other):
        if not isinstance(other, PluginConfig):
            return self

        for key in other.keys():
            self.modified = True if key != PluginConfig.GLOBAL_KEY else False
            self[key] = other[key]

        return self

    def __sub__(self, other):
        """
        Remove the keys of the other config
        :param other:
        :return:
        """
        if self is other or not isinstance(other, PluginConfig):
            return self

        for key in other.keys():
            if key in self:
                self.modified = True if key != PluginConfig.GLOBAL_KEY else False
                del self[key]

        return self

    def __len__(self):
        return len(list(filter(lambda x: x != PluginConfig.GLOBAL_KEY,
                               self._config.keys())))

    def set_global_config(self, config):
        self[PluginConfig.GLOBAL_KEY] = config

    def get_global_config(self):
        return self[PluginConfig.GLOBAL_KEY]

    def keys(self):
        return self._config.keys()

    def to_json(self):
        """
        Converts the config values to a JSON string
        :return: JSON string
        :rtype: str
        """
        return json.dumps(self._config, indent=True)

    @classmethod
    def create_from_dict(cls, dict):
        """
        Factory method to create a PluginConfig from a python dictionary
        :param dict:
        :return: a PluginConfig
        :rtype: py:class:`toolbox.config.PluginConfig`
        """

        config = cls()
        for k in dict:
            config[k] = dict[k]

        return config
