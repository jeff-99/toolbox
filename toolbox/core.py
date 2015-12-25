import argparse
from .registry import Registry
from .scanner import find_contrib_modules, find_modules, find_local_modules
from .config import ConfigManager
from .mixins import ConfigMixin


class UnknownPlugin(Exception):
    pass


class Toolbox(object):
    
    def __init__(self, external=True, local=True):

        # load core plugins
        modules = find_contrib_modules()

        self.registry = Registry()
        self.registry.populate(modules)
        self.parser = argparse.ArgumentParser()

        global_config = self.registry.get_plugin('config').get_config()

        extra_modules = []
        if external:
            extra_modules += find_modules(global_config['toolbox_prefix'])
        if local:
            extra_modules += find_local_modules(global_config['local_plugin_dir'])

        self.registry.populate(extra_modules)

    def prepare(self):
        # prepare main parser
        self.parser.usage = '%(prog)s tool [args]'
        self.parser.description = 'Extendable plugin toolbox'

        # prepare subparsers
        subparsers = self.parser.add_subparsers(help='Plugins', dest='plugin')

        for plugin in self.registry.get_plugins():
            # create a new subparser for this plugin
            plugin_parser = subparsers.add_parser(plugin.name)

            # set the default execute method as plugin executable
            plugin_parser.set_defaults(executable=plugin.execute)

            # let the plugin prepare the arguments
            plugin.prepare_parser(plugin_parser)


    def execute(self, args):
        parsed_args = self.parser.parse_args(args)

        if parsed_args.plugin is None:
            self.parser.print_help()
            raise UnknownPlugin('Plugin not set')
        else:
            # triggers the lazy loading of the selected plugin
            self.registry.get_plugin(parsed_args.plugin)
        try:
            parsed_args.executable(parsed_args)
        except Exception as e:
            print("Somehow the plugin did not do what it should have done!")
            print(e)

    def shutdown(self):
        self.registry.shutdown()

