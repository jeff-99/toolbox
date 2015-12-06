__author__ = 'jeff'

from toolbox.plugin import BasePlugin


Plugin = BasePlugin('example','this is an example plugin')
Plugin.set_execute(print)

