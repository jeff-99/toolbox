__author__ = 'jeff'

from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import ConfigMixin
import pip, re, os, shutil, inspect, importlib

class InstallPlugin (ConfigMixin, ToolboxPlugin):

    name = 'install'
    description = 'Install a toolbox plugin from pypi or git'

    def prepare_parser(self, parser):
        parser.add_argument("-u","--uninstall", action="store_true", help="Uninstall plugin")
        parser.add_argument("-l", "--local", action='store_true', help="Install locally")
        parser.add_argument("-e", "--enable", action="store_true", help="enable existing package as toolbox plugin")
        parser.add_argument("-d", "--disable", action="store_true", help="disable an symlinked package")
        parser.add_argument("package")


    def execute(self, args):
        if not hasattr(args, 'package'):
            print('No package selected')

        command = 'install' if not args.uninstall else "uninstall"

        # check if given package is a local directory
        if os.path.exists(args.package):
            local_dir = self.get_config()['local_plugin_dir']
            if command == 'install':
                try:
                    name = args.package.split('/')[-1]
                    shutil.copytree(args.package,os.path.join(local_dir,name))
                except Exception as e:
                    print('Installation of {} failed with : {}'.format(args.package,e))
            elif command == 'uninstall':
                try:
                    name = args.package.split('/')[-1]
                    shutil.rmtree(os.path.join(local_dir,name))
                except Exception as e:
                    print('Installation of {} failed with : {}'.format(args.package,e))


        # not a local dir let pip do the heavy lifting
        else:
            pip.main([command, args.package])

        # check if enable flag is set and if any of the installed packages contains the name of the module provided
        if (args.enable or args.disable) and any([args.package in package.key for package in pip.get_installed_distributions()]):
            # find the package directory
            m = importlib.import_module(args.package)
            module_dir = os.path.dirname(inspect.getfile(m))
            symlink = os.path.join(self.get_config()['local_plugin_dir'], args.package)

            if args.enable:
                # symlink the directory in the local plugin dir
                os.symlink(module_dir,symlink , True)
                print("{} is enabled to use with Toolbox".format(args.package))

            if args.disable:
                os.unlink(symlink)
                print("{} is disabled".format(args.package))
