__author__ = 'jeff'

from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import RegistryMixin
from toolbox.scanner import find_modules
from terminaltables import AsciiTable

class ListPlugin(RegistryMixin, ToolboxPlugin):
    name = 'list'
    description = 'List all plugins'

    def prepare_parser(self, parser):
        parser.add_argument('-e','--external',action='store_true',help='only external plugins')

    def execute(self, args):
        registry = self.get_registry()


        data = []
        if args.external:
            for name in find_modules():
                data.append([name,''])
        else:
            for plugin in registry.get_plugins():
                data.append([plugin.name,plugin.description])

        data.sort(key=lambda row: row[0])
        data.insert(0,['Plugin', 'Description'])

        table = AsciiTable(data)
        table.padding_left = 3
        table.padding_right = 3
        print(table.table)