__author__ = 'jeff'
import pip
import re
import os
import sys


MODULE_PREFIX = 'tbx_'
LOCAL_PLUGIN_PATH = os.path.join(os.path.expanduser('~'), '.toolbox/plugins')


def find_contrib_modules():
    contrib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contrib')
    modules = []
    for module_name in os.listdir(contrib_dir):
        if os.path.isdir(os.path.join(contrib_dir,module_name)) and not str(module_name).startswith("__"):
            modules.append("toolbox.contrib.{}".format(module_name))
    return modules


def find_local_modules(plugin_dir):
    if plugin_dir is None or not os.path.isdir(plugin_dir):
        return []

    sys.path.append(plugin_dir)

    modules = []
    for module_name in os.listdir(plugin_dir):
        if os.path.isdir(os.path.join(plugin_dir,module_name)) and not str(module_name).startswith("__"):
            modules.append(module_name)
    return modules


def find_modules(prefix=None):
    """
    Returns a list of importable modules
    :return:
    """
    if prefix is None:
        prefix = ''

    installed_modules = pip.get_installed_distributions()
    modules = []
    for module in installed_modules:
        match = re.match(r'{}\w+'.format(prefix), module.key)
        if not match is None:
            modules.append(module.key)

    return modules



if __name__ == '__main__':
    # print(sys.modules)
    find_contrib_modules()
    # find_modules()
    # pass