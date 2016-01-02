__author__ = 'jeff'
import toolbox.plugin

class TestPlugin(toolbox.plugin.ToolboxPlugin):
    name = 'test'
    description = 'test'

    def prepare_parser(self, parser):
        pass

    def execute(self, args):
        pass