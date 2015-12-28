__author__ = 'jeff'


from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import ConfigMixin, RegistryMixin
from toolbox.utils import generate_name
from .parser import Parser
import os, tempfile, zipfile, shutil

class CreatePlugin(RegistryMixin, ConfigMixin, ToolboxPlugin):
    name = 'create'
    description = 'Create a new plugin'

    def prepare_parser(self, parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-i', '--install', action='store_true', help="Create and directly install new plugin")
        group.add_argument('-d','--dir', type=str, help='Source directory of your new plugin')

        parser.add_argument('-t', '--template', choices=['default', 'shell'], default='default')
        parser.add_argument('name', type=str, help='Name of your new plugin', default=generate_name(), nargs="?")

    def execute(self, args):
        context = {}
        context['toolname'] = args.name
        template_src = os.path.join(os.path.dirname(__file__), 'templates', args.template + ".zip")

        temp_dir =tempfile.mkdtemp()
        zipfile.ZipFile(template_src).extractall(temp_dir)

        template_path = os.path.join(os.path.join(temp_dir,args.template))

        dest_dir = os.path.abspath(args.dir) if not args.dir is None else os.getcwd()

        if args.template == 'shell':
            command = input('Command to be executed by this plugin: ')
            executable, *argv = command.split(' ')
            context["executable"] = executable
            context["args"] = argv

            if args.install:
                dest_dir = self.get_global_config()['local_plugin_dir']

        p = Parser(template_path, dest_dir, context)

        for (dir, files, file_contents) in p.parse():
            if not os.path.exists(dir):
                os.mkdir(dir)

            for i, fp in enumerate(files):
                with open(os.path.join(dir, fp), 'w') as f:
                    f.write(file_contents[i])

        # remove tmp dir
        shutil.rmtree(temp_dir)

