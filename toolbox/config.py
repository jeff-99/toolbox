import os
import json
import collections
from .mixins import ConfigMixin
from .defaults import *
import copy


class ConfigManager(object):

    FILE_EXT = '.json'

    def __init__(self):
        if not os.path.isdir(TOOLBOX_DIR):
            os.mkdir(TOOLBOX_DIR)

        if not os.path.isdir(CONF_DIR):
            os.mkdir(CONF_DIR)

        self.config_dir =  CONF_DIR

        # config plugin's config is global config
        self._settings_file = os.path.join(
                            CONF_DIR,
                            'config' + ConfigManager.FILE_EXT)

        if not os.path.exists(self._settings_file):
            with open(self._settings_file, 'w') as f:
                json.dump({
                    'toolbox_dir' : TOOLBOX_DIR,
                    'config_dir' : CONF_DIR,
                    'local_plugin_dir' : LOCAL_PLUGIN_DIR,
                    'toolbox_prefix' : TOOLBOX_PREFIX
                },f)

        with open(self._settings_file, 'r') as f:
            self._global_config = PluginConfig.create_from_dict(json.load(f))

    def load_plugin(self, name):
        file_name = name + ConfigManager.FILE_EXT
        path = os.path.join(self.config_dir,file_name)

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

        global_conf = self.get_global_config()
        plugin_config.set_global_config(global_conf)
        return plugin_config


    def save_plugin(self,name, config):
        file_name = name + ConfigManager.FILE_EXT
        path = os.path.join(self.config_dir,file_name)

        if os.path.exists(path) and not os.path.isfile(path):
            raise Exception('path exists but it ain\'t a file Brah')

        del config[PluginConfig.GLOBAL_KEY]

        self._save_config(path, config)

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

    def merge_configs(self,base, *args):
        """
        Merge config with global configs
        :param base:
        :param args:
        :return:
        """
        config = copy.deepcopy(base)
        for c in args:
            config = config + c
        return config

    def remove_config(self, base, *args):
        """
        Remove global config variables
        :param base:
        :param args:
        :return:
        """
        config = copy.deepcopy(base)
        for c in args:
            config = config - c

        return config


class PluginConfig(object):

    GLOBAL_KEY = '__GLOBAL__'

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

    def __add__(self, other):
        if not isinstance(other, PluginConfig):
            return self

        for key in other.keys():
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
                del self[key]

        return self

    def set_global_config(self, config):
        self[PluginConfig.GLOBAL_KEY] = config

    def get_global_config(self):
        return self[PluginConfig.GLOBAL_KEY]

    def keys(self):
        return self._config.keys()

    def to_json(self):
        return json.dumps(self._config, indent=True)

    @classmethod
    def create_from_dict(cls, dict):

        config = cls()
        for k in dict:
            config[k] = dict[k]

        return config