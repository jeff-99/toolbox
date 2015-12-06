__author__ = 'jeff'

from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import ConfigMixin
import pip

class InstallPlugin (ConfigMixin, ToolboxPlugin):

    name = 'install'
    description = 'Install a toolbox plugin from pypi or git'

    def prepare_parser(self, parser):
        parser.add_argument("-u","--uninstall",help="Uninstall plugin")
        parser.add_argument("package")


    def execute(self, args):
        if not hasattr(args, 'package'):
            print('No package selected')

        command = 'install' if args.uninstall is None else 'uninstall'
        pip.main([command, args.package])