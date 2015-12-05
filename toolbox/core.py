__author__ = 'jeff'

import argparse
from .registry import Registry
from .scanner import find_contrib_modules, find_modules

class Toolbox(object):
    registry = Registry()
    parser = argparse.ArgumentParser()
    
    def __init__(self, external=True,contrib=True):

        modules = []
        if contrib:
            modules += find_contrib_modules()
        if external:
            modules += find_modules()

        self.registry.populate(modules)

    def prepare(self):
        self.parser.add_argument("--list",action="store_true",help="list all plugins")
        subparsers = self.parser.add_subparsers(help='Plugins')

        for plugin in self.registry.get_plugins():
            # create a new subparser for this plugin
            plugin_parser = subparsers.add_parser(plugin.name)

            # set the default execute method as plugin executable
            plugin_parser.set_defaults(executable=plugin.execute)

            # let the plugin prepare the arguments
            plugin.prepare_parser(plugin_parser)

    def execute(self, args):
        parsed_args = self.parser.parse_args(args)

        if parsed_args.list:
            for n in self.registry.get_plugin_names():
                print(n)
            return

        try:
            parsed_args.executable(parsed_args)
        except Exception as e:
            print("Somehow the plugin did not do what it should have done!")
            print(e)

