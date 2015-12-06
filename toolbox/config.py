__author__ = 'jeff'
import os
import json
import collections
from .mixins import ConfigMixin

class ConfigManager(object):

    TOOLBOX_DIR = '.toolbox'
    CONFIG_DIR = 'config'
    FILE_EXT = '.json'

    def __init__(self):
        toolbox_dir = os.path.join(os.path.expanduser('~'), ConfigManager.TOOLBOX_DIR)
        config_dir = os.path.join(toolbox_dir, ConfigManager.CONFIG_DIR)

        if not os.path.isdir(toolbox_dir):
            os.mkdir(toolbox_dir)

        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

        self.config_dir = config_dir

        # config plugin's config is global config
        self._settings_file = os.path.join(
                            os.path.expanduser('~'),
                            ConfigManager.TOOLBOX_DIR,
                            ConfigManager.CONFIG_DIR,
                            'config' + ConfigManager.FILE_EXT)

        if not os.path.exists(self._settings_file):
            with open(self._settings_file, 'w') as f:
                json.dump({},f)

        with open(self._settings_file, 'r') as f:
            self._global_config = PluginConfig.create_from_dict(json.load(f))

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

        self._save_config(path,config)

    def save(self, plugins):
        for plugin in plugins:
            if isinstance(plugin, ConfigMixin):
                self.save_plugin(plugin.name, plugin.get_config())

    def get_global_config(self):
        return self._global_config

    def save_global_config(self):
        self._save_config(self._settings_file, self._global_config)

    def _save_config(self, fp, config):
        with open(fp, 'w') as f:
            f.write(config.to_json())


class PluginConfig(object):

    def __init__(self):
        self._config = collections.defaultdict(lambda: None)

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __delitem__(self, key):
        del self._config[key]

    def __contains__(self, item):
        return item in self._config

    def to_json(self):
        return json.dumps(self._config, indent=True)

    @classmethod
    def create_from_dict(cls, dict):

        config = cls()
        for k in dict:
            config[k] = dict[k]

        return config
