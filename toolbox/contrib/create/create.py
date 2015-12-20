__author__ = 'jeff'


from toolbox.plugin import ToolboxPlugin
from .parser import Parser
import os

class CreatePlugin(ToolboxPlugin):
    name = 'create'
    description = 'Create a new plugin'

    def prepare_parser(self, parser):
        parser.add_argument('name', type=str, help='Name of your new plugin')
        parser.add_argument('dir', type=str, help='Source directory of your new plugin')

    def execute(self, args):

        name = args.name
        p = Parser(os.path.join(os.path.dirname(__file__), 'template'),args.dir,{'toolname':name})

        for (dir, files, file_contents) in p.parse():
            if not os.path.exists(dir):
                os.mkdir(dir)

            for i, fp in enumerate(files):
                with open(os.path.join(dir, fp), 'w') as f:
                    f.write(file_contents[i])


