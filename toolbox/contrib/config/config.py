__author__ = 'jeff'

from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import ConfigMixin

class ConfigPlugin (ConfigMixin, ToolboxPlugin):
    name = 'config'
    description = 'Config API'

    def prepare_parser(self, parser):
        parser.add_argument('method', choices=['set','get'])
        parser.add_argument('attribute', type=str)
        parser.add_argument('value', nargs='?')

    def execute(self, args):
        config = self.get_config()

        if args.method == 'set' and not args.value is None:
            config[args.attribute] = args.value
        elif args.method == 'get':
            print("Attribute {} is set to {}".format(args.attribute,config[args.attribute]))
