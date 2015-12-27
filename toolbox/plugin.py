__author__ = 'jeff'
from abc import ABCMeta, abstractmethod, abstractproperty
import subprocess, os

class ToolboxPlugin(object):
    """
    Abstract base class for an Toolbox plugin
    """
    __metaclass__ = ABCMeta

    name = None
    description = None

    @abstractmethod
    def prepare_parser(self, parser):
        pass

    @abstractmethod
    def execute(self, args):
        pass

class NotCallableException (Exception):
    pass


class BasePlugin(ToolboxPlugin):
    """
    An easy to use Plugin wrapper that sets all the necessary parts of a ToolboxPlugin

    :param name: The name of the plugin
    :param description: short description of the plugin (used to index and search plugins)
    :param prepare_parser_func: The function that prepares the Toolbox main parser
    :param execute_func: the main function of the plugin, accecpts :py:class:`argparse.Namespace`
    :return:
    """
    def __init__(self,name, description=None, prepare_parser_func=None, execute_func=None):
        if not prepare_parser_func is None:
            self.set_prepare_parser(prepare_parser_func)
        if not execute_func is None:
            self.set_execute(execute_func)

        self.name = name
        self.description = description

    def set_prepare_parser(self, prepare_parser_func):
        """
        Set the callable that prepares the Toolbox parser.
        the callable gets a argparse.Argumentparser as argument

        :param parser:
        :type parser: function
        :raise: py:class:`toolbox.plugin.NotCallableException`
        :return:
        """
        if hasattr(prepare_parser_func, '__call__'):
            self.prepare_parser_func = prepare_parser_func
        else:
            raise NotCallableException("{} is not callable".format(prepare_parser_func))

    def set_execute(self, execute_func):
        """
        Set the executable for the toolbox.
        the executable gets passed a ArgumentParser Namespace

        :param parser:
        :type parser: function
        :raise: py:class:`toolbox.plugin.NotCallableException`
        :return:
        """
        if hasattr(execute_func, '__call__'):
            self.execute_func = execute_func
        else:
            raise NotCallableException("{} is not callable".format(execute_func))

    def set_description(self,description):
        self.description = description

    def prepare_parser(self, parser):
        try:
            return self.prepare_parser_func(parser)
        except AttributeError:
            pass
        except TypeError:
            pass


    def execute(self, args):
        try:
            return self.execute_func(args)
        except AttributeError:
            pass
        except TypeError:
            pass


class ExecutablePlugin(ToolboxPlugin):
    """
    The ExecutablePlugin is a basic plugin to register shell scripts and the like.
    Just subclass it and provide the following attributes:
     - name
     - description (optional)
     - executable (the main executable)
     - args (a list of default arguments)

    optionally the prepare_parser and execute methods can be overridden to add exta functionality
    """
    name = None
    description = None
    executable = None
    args = []

    def prepare_parser(self, parser):
        parser.add_argument('args', nargs="*")

    def execute(self, args):
        if self.executable is None:
            raise ValueError('executable path can not be empty')

        executable = os.path.abspath(self.executable) if os.path.exists(self.executable) else self.executable

        command = [executable] + self.args + args.args
        subprocess.call(command)

    def setup(self, name, executable, **kwargs):
        """
        Method to setup an Executable plugin, no need to subclass it this way!

        :param name:
        :param executable:
        :param kwargs:
        :return:
        """
        self.name = name
        self.executable = executable

        if 'description' in kwargs:
            self.description = kwargs['description']

        if 'args' in kwargs:
            self.args = kwargs['args']


