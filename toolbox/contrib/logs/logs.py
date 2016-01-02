from toolbox.plugin import ToolboxPlugin
from toolbox.defaults import TOOLBOX_DIR
import os, re

class LogsPlugin(ToolboxPlugin):
    name = 'logs'
    description = 'view logs'

    def prepare_parser(self, parser):
        parser.add_argument('pluginlog', nargs="?", help="filter for plugin")

    def execute(self, args):
        with open(os.path.join(TOOLBOX_DIR, 'toolbox.log'), 'r') as f:
            for line in f.readlines():
                if args.pluginlog is not None:
                    pattern = 'toolbox.plugins.{}'.format(args.pluginlog)
                    match = re.search(re.escape(pattern), line, re.IGNORECASE)
                    if not match is None:
                        print(line.rstrip('\n'))
                else:
                    print(line.rstrip('\n'))
