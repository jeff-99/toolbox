__author__ = 'jeff'
import pip
import re
import os


MODULE_PREFIX = 'toolbox_'

def find_contrib_modules():
    contrib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contrib')
    modules = []
    for module_name in os.listdir(contrib_dir):
        if os.path.isdir(os.path.join(contrib_dir,module_name)) and not str(module_name).startswith("__"):
            modules.append("toolbox.contrib.{}".format(module_name))
    return modules


def find_modules():
    """
    Returns a list of importable modules
    :return:
    """
    installed_modules = pip.get_installed_distributions()
    modules = []
    for module in installed_modules:
        match = re.match(r'{}\w+'.format(MODULE_PREFIX), module.key)
        if not match is None:
            modules.append(module.key)

    return modules



if __name__ == '__main__':
    # print(sys.modules)
    find_contrib_modules()
    # find_modules()
    # pass