__author__ = 'jeff'

from toolbox.plugin import ToolboxPlugin
from toolbox.mixins import ConfigMixin, RegistryMixin
from toolbox.scanner import find_local_modules
import pip, os, shutil, inspect, importlib, hashlib

class InstallPlugin (RegistryMixin, ConfigMixin, ToolboxPlugin):

    name = 'install'
    description = 'Install a toolbox plugin from pypi or git'

    def prepare_parser(self, parser):
        parser.add_argument("-u", "--uninstall", action="store_true", help="Uninstall plugin")
        parser.add_argument("-d", "--dev", action='store_true', help="Install a dev plugin")
        parser.add_argument("-e", "--external", action="store_true", help="enable an existing python package as toolbox plugin")
        parser.add_argument("--disable-only", action="store_true", help="Option to only disable the external module for the toolbox, not uninstall it")
        parser.add_argument("package")


    def execute(self, args):
        if not hasattr(args, 'package'):
            print('No package selected')

        command = 'install' if not args.uninstall else "uninstall"

        # check if given package is a local directory
        if os.path.exists(args.package):

            src_dir = os.path.abspath(args.package)
            package_name = args.package.split('/')[-1] if not args.dev else hashlib.md5(src_dir.encode('utf-8')).hexdigest()

            if command == 'install':
                self.local_install(src_dir,package_name,args.dev)

            if command == 'uninstall':
                self.local_uninstall(package_name,args.dev)

        elif command == 'uninstall' and args.package in find_local_modules(self.get_global_config()['local_plugin_dir']):
            # uninstall local plugins by name
            self.local_uninstall(args.package)

        elif not args.disable_only:
            # not a local dir let pip do the heavy lifting
            pip.main([command, args.package])

        # check if external flag is set and if any of the installed packages contains the name of the module provided
        if args.external and any([args.package in package.key for package in pip.get_installed_distributions()]):
            config_tool = self.get_registry().get_plugin('config')
            external_plugins = set(config_tool.get('external_plugins') or [])

            if command == "install":
                external_plugins.add(args.package)
                message = "{} is enabled to use with Toolbox"
            else:
                external_plugins.remove(args.package)
                message = "{} is uninstalled to use with Toolbox"

            config_tool.set('external_plugins', list(external_plugins))
            print(message.format(args.package))

    def local_install(self,src_dir, package_name, dev=False):
        """
        Install a package from source with the given name
        If dev == True a symlink is created instead for development
        :param str src_dir:
        :param str package_name:
        :param bool dev:
        :return:
        """
        local_dir = self.get_global_config()['local_plugin_dir']
        dest_dir = os.path.join(local_dir, package_name)

        if dev:
            os.symlink(dest_dir,src_dir , True)
        else:
            try:
                shutil.copytree(src_dir,dest_dir)
            except Exception as e:
                print('Installation of {} failed with : {}'.format(src_dir,e))

    def local_uninstall(self,package_name, dev=False):
        """
        Uninstall a locally installed plugin
        If dev == True the symlink is deleted
        :param package_name:
        :param dev:
        :return:
        """
        local_dir = self.get_global_config()['local_plugin_dir']
        dest_dir = os.path.join(local_dir, package_name)

        if dev:
            os.unlink(dest_dir)
        else:
            try:
                shutil.rmtree(dest_dir)
            except Exception as e:
                print('Installation of {} failed with : {}'.format(dest_dir,e))

