import unittest
from toolbox.plugin import BasePlugin, ToolboxPlugin
from toolbox.mixins import RegistryMixin, ConfigMixin, LogMixin
from toolbox.registry import Registry, NoPluginException
from toolbox.config import PluginConfig
from logging import Logger


class CompleteTool(ConfigMixin, LogMixin, RegistryMixin, BasePlugin):
    pass

class ImportedPlugin(ToolboxPlugin):
    name = 'test'
    description = 'test'

    def prepare_parser(self, parser):
        pass

    def execute(self, args):
        pass


class TestRegistry(unittest.TestCase):

    def setUp(self):
        self.test_plugin = BasePlugin('test_tool','testing tool',prepare_parser_func=print, execute_func=print)

    def tearDown(self):
        pass

    def test_add_valid_plugin(self):
        registry = Registry()
        self.assertEqual(registry.add_plugin(self.test_plugin), None)

    def test_add_non_toolboxplugin(self):
        registry = Registry()
        with self.assertRaises(NoPluginException):
            registry.add_plugin(Registry())

    def test_add_nameless_plugin(self):
        registry = Registry()
        plugin = BasePlugin('test', None, print, print)
        del plugin.name

        with self.assertRaises(AttributeError):
            registry.add_plugin(plugin)

    def test_populate_valid_modules(self):
        registry = Registry()
        registry.populate(['toolbox.contrib.list', 'toolbox.contrib.create'])

        self.assertEqual(len(registry.get_plugin_names()),2)

    def test_populate_string(self):
        registry = Registry()
        with self.assertRaises(ImportError):
            registry.populate('toolbox.contrib.list')

    def test_populate_class(self):
        registry = Registry()
        registry.populate(['tests.plugin_module'])


    def test_populate_invalid_tools(self):
        registry = Registry()
        with self.assertRaises(AttributeError):
            registry.populate([self.test_plugin])


    def test_get_tool_names(self):
        registry = Registry()
        registry.add_plugin(BasePlugin('plugin1', 'desc1', print, print))
        registry.add_plugin(BasePlugin('plugin2', 'desc2', print, print))

        self.assertEqual(sorted(registry.get_plugin_names()), sorted(['plugin1', 'plugin2']))
    
    def test_get_plugins_return_plugins(self):
        registry = Registry()
        first = BasePlugin('plugin1', 'desc1', print, print)
        second = BasePlugin('plugin2', 'desc2', print, print)
        registry.add_plugin(first)
        registry.add_plugin(second)

        original = sorted([first,second], key=lambda x: x.name)
        for i, plugin in enumerate(sorted(registry.get_plugins(), key=lambda x: x.name)):
            self.assertIs(plugin, original[i])
        
    def test_get_plugins_length(self):
        registry = Registry()
        first = BasePlugin('plugin1', 'desc1', print, print)
        second = BasePlugin('plugin2', 'desc2', print, print)
        registry.add_plugin(first)
        registry.add_plugin(second)

        self.assertCountEqual(registry.get_plugins(), [first,second])

    def test_get_plugin(self):
        registry = Registry()
        first = BasePlugin('plugin1', 'desc1', print, print)
        registry.add_plugin(first)

        self.assertIs(registry.get_plugin('plugin1'),first)

    def test_get_non_existing_plugin(self):
        registry = Registry()
        with self.assertRaises(ValueError):
            registry.get_plugin('testing')

    def test_get_loaded_plugin(self):
        registry = Registry()
        first = BasePlugin('plugin1', 'desc1', print, print)
        registry.add_plugin(first)

        self.assertIs(registry.get_plugin('plugin1'),first)
        self.assertIs(registry.get_plugin('plugin1'),first)

    def test_load_plugin(self):
        registry = Registry()
        tool = CompleteTool('plugin1', 'complete', print,print)

        registry.add_plugin(tool)

        registry.populate(['toolbox.contrib.config'])
        registry.get_plugin('config')

        loaded_plugin = registry.get_plugin('plugin1')

        self.assertIsInstance(loaded_plugin.get_config(), PluginConfig)

        self.assertIsInstance(loaded_plugin.get_registry(), Registry)

        self.assertIsInstance(loaded_plugin.get_logger(), Logger)

