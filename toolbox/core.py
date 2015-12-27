import argparse
from .registry import Registry, NoPluginException
from .scanner import find_contrib_modules, find_modules, find_local_modules
from .config import ConfigManager
from .mixins import ConfigMixin


class UnknownPlugin(Exception):
    pass


class Toolbox(object):
    """
        Initialize the toolbox, sets up the main argument parser and Tool registry
        Core tools in de contrib package are always loaded

        The local and external flags can be used to limit the loaded modules

        :param bool external:
        :param bool local:
        :return:
        """
    
    def __init__(self, external=True, local=True):
        # load core plugins
        modules = find_contrib_modules()

        self.registry = Registry()
        self.registry.populate(modules)
        self.parser = argparse.ArgumentParser()

        global_config = self.registry.get_plugin('config')

        extra_modules = []
        if external:
            extra_modules += find_modules(global_config.get('toolbox_prefix'))
            extra_modules += global_config.get('external_plugins')
        if local:
            extra_modules += find_local_modules(global_config.get('local_plugin_dir'))

        try:
            self.registry.populate(extra_modules)
        except (AttributeError, NoPluginException) as e:
            print("An external Plugin caused trouble, please uninstall it -- {}".format(e))


    def prepare(self):
        """
        Prepares the main Argument parser by loading all registered plugins and setting their executable

        :return:
        """
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
        """
        This is the Toolbox's main function which parses the arguments, which should yield:
         - a Tool
         - an Executable
         - and some optional arguments

        The Tool gets fetched from the registry where it will be fully loaded
         and the exectuble is executed with the remaining args
        :param args: List of arguments
        :type args: list
        :return:
        """
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
        """
        Shuts down the application, save and close config files etc.
        :return:
        """
        self.registry.shutdown()

    def __call__(self, args):
        """
        Run the Toolbox with the supplied arguments.
        This method is primarily used by the commandline script

        :param args:
        :return:
        """
        self.prepare()

        try:
            self.execute(args)
        except UnknownPlugin:
            return

        self.shutdown()

