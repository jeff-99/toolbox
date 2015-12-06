__author__ = 'jeff'

import argparse
from .registry import Registry
from .scanner import find_contrib_modules, find_modules
from .config import ConfigManager
from .mixins import ConfigMixin

class Toolbox(object):
    
    def __init__(self, external=True,contrib=True):

        modules = []
        if contrib:
            modules += find_contrib_modules()
        if external:
            modules += find_modules()

        self.registry = Registry()
        self.parser = argparse.ArgumentParser()
        self.config_manager = ConfigManager()

        self.registry.populate(modules)
        self._active_plugin = None

    def prepare(self):
        subparsers = self.parser.add_subparsers(help='Plugins', dest='plugin')

        for plugin in self.registry.get_plugins():
            # create a new subparser for this plugin
            plugin_parser = subparsers.add_parser(plugin.name)

            # set the default execute method as plugin executable
            plugin_parser.set_defaults(executable=plugin.execute)

            # let the plugin prepare the arguments
            plugin.prepare_parser(plugin_parser)


    def _load_plugin(self, name):
        plugin = self.registry.get_plugin(name)

        if isinstance(plugin, ConfigMixin):
            config = self.config_manager.load_plugin(plugin.name)
            plugin.set_config(config)

    def execute(self, args):
        parsed_args = self.parser.parse_args(args)


        if parsed_args.plugin is None:
            raise Exception('Plugin not set')
        else:
            self._active_plugin = parsed_args.plugin
            self._load_plugin(parsed_args.plugin)

        try:
            parsed_args.executable(parsed_args)
        except Exception as e:
            print("Somehow the plugin did not do what it should have done!")
            print(e)

    def shutdown(self):
        active_plugin = self.registry.get_plugin(self._active_plugin)
        if isinstance(active_plugin, ConfigMixin):
            self.config_manager.save_plugin(active_plugin.name, active_plugin.get_config())

