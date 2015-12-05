__author__ = 'jeff'
import os
import json
import pathlib
from .mixins import ConfigMixin

class ConfigManager(object):

    CONFIG_DIR = '.toolbox'
    FILE_EXT = '.json'

    def __init__(self):
        config_dir = os.path.join(os.path.expanduser('~'), ConfigManager.CONFIG_DIR)

        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

        self.config_dir = config_dir

    def load_plugin(self, name):
        file_name = name + ConfigManager.FILE_EXT
        path = os.path.join(self.config_dir,file_name)

        if not os.path.exists(path):
            return PluginConfig()
        elif os.path.exists(path) and not os.path.isfile(path):
            raise TypeError('{} is not a file'.format(path))
        else:
            with open(path, 'r') as f:
                try:
                    config = json.load(f)
                    plugin_config = PluginConfig.create_from_dict(config)

                    return plugin_config
                except ValueError:
                    return PluginConfig()



    def save_plugin(self,name, config):
        file_name = name + ConfigManager.FILE_EXT
        path = os.path.join(self.config_dir,file_name)

        if os.path.exists(path) and not os.path.isfile(path):
            raise Exception('path exists but it ain\'t a file Brah')

        with open(path , 'w') as f:
            json.dump(config._config, f)

    def save(self, plugins):
        for plugin in plugins:
            if isinstance(plugin, ConfigMixin):
                self.save_plugin(plugin.name, plugin.get_config())



class PluginConfig(object):

    _config = {}

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __missing__(self,key):
        return None

    def __delitem__(self, key):
        del self._config[key]

    def __contains__(self, item):
        return item in self._config

    @classmethod
    def create_from_dict(cls, dict):

        config = cls()
        for k in dict:
            config[k] = dict[k]

        return config
