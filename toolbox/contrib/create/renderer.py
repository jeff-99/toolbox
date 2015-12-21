import os

def capitalize(string):
    return string.capitalize()

def pylist(param):
    """
    Takes a comma separated string or list and renders a python list source code
    :param param:
    :return:
    """
    prefix = '["'
    suffix = '"]'
    if isinstance(param,str):
        param = param.split(' ')

    if isinstance(param,list):
        param = '","'.join(param)

    return prefix + param + suffix

def path(string):
    return os.path.abspath(string)

ALIASES = {
    'c': capitalize,
    'path': path,
    'pylist': pylist
}
