__author__ = 'jeff'
from abc import ABCMeta, abstractmethod, abstractproperty

class ToolboxPlugin(object):
    __metaclass__ = ABCMeta

    name = None

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
    """
    def __init__(self,name = None, description = None, prepare_parser_func = None, execute_func = None):
        if not prepare_parser_func is None:
            self.set_prepare_parser(prepare_parser_func)
        if not execute_func is None:
            self.set_execute(execute_func)

        self.name = name
        self.description = description

    def set_prepare_parser(self, prepare_parser_func):
        if hasattr(prepare_parser_func, '__call__'):
            self.prepare_parser_func = prepare_parser_func
        else:
            raise NotCallableException("{} is not callable".format(prepare_parser_func))

    def set_execute(self, execute_func):
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
