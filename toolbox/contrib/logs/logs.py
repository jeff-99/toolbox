from toolbox.plugin import ToolboxPlugin
from toolbox.defaults import TOOLBOX_DIR
import os

class LogsPlugin(ToolboxPlugin):
    name = 'logs'
    description = 'view logs'

    def prepare_parser(self, parser):
        parser.add_argument('tool', nargs="?", help="filter for plugin")

    def execute(self, args):
        if args.tool is not None:
            pass
        else:
            with open(os.path.join(TOOLBOX_DIR, 'toolbox.log~'), 'r') as f:
                [print(line.rstrip('\n')) for line in f.readlines()]