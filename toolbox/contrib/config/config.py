__author__ = 'jeff'

from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import ConfigMixin
from toolbox.defaults import *


class ConfigPlugin(ConfigMixin, ToolboxPlugin):
    name = 'config'
    description = 'Config API holds and controls the global config'

    def prepare_parser(self, parser):
        parser.add_argument('method', choices=['set', 'get'])
        parser.add_argument('attribute', type=str)
        parser.add_argument('value', nargs='?')

    def execute(self, args):
        if args.method == 'set' and not args.value is None:
            self.set(args.attribute, args.value)
        elif args.method == 'get':
            print("Attribute {} is set to {}".format(args.attribute, self.get(
                args.attribute)))

    def set(self, key, value):
        self.get_config()[key] = value

    def get(self, key):
        return self.get_config()[key]

    def set_defaults(self):
        """
        Sets the default config variables, used when toolbox is used for the first time
        :return:
        """
        self.set('toolbox_dir', TOOLBOX_DIR)
        self.set('config_dir', CONF_DIR)
        self.set('local_plugin_dir', LOCAL_PLUGIN_DIR)
        self.set('toolbox_prefix', TOOLBOX_PREFIX)
        self.set('external_plugins', [])
