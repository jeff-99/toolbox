===============================
Toolbox
===============================

.. image:: https://img.shields.io/pypi/v/tool-box.svg
        :target: https://pypi.python.org/pypi/tool-box

.. image:: https://img.shields.io/travis/jeff-99/toolbox.svg
        :target: https://travis-ci.org/jeff-99/toolbox

.. image:: https://readthedocs.org/projects/toolbox/badge/?version=latest
        :target: https://readthedocs.org/projects/tool-box/?badge=latest
        :alt: Documentation Status


What is Toolbox ?
-----------------

Toolbox is a framework to manage a collection of tools.
A tool can be anything from a shell script to a python package.

Basically toolbox extends the python argparse.ArgumentParser to enable importing tools from multiple locations
in a single executable. Toolbox provides some easy default tools to create , install, uninstall or list (available) tools.

A custom tool needs to implement 2 methods:
* prepare_parser : which prepares an argparse.ArgumentParser
* execute : which is the main entry point of your tool

Besides the wrapper around argument parsing toolbox as a framework provides some easy to add extra's like persisted configuration,
usage of tools within tools and no-configuration logging.

An example of a custom tool::

        from toolbox.plugin import ToolboxPlugin
        from toolbox.mixins import RegistryMixin, ConfigMixin, LogMixin

        class CustomPlugin(RegistryMixin, ConfigMixin, LogMixin, ToolboxPlugin)
                name = "custom"
                description = "This is a custom plugin that prints a string"

                def prepare_parser(self,parser):
                        parser.add_argument('printable', help="string to print")

                def execute(args):
                        # LogMixin
                        logger = self.get_logger()
                        logger.info("printing {}".format(args.printable)

                        # ConfigMixin
                        config = self.get_config()
                        config['first_print'] = args.printable

                        # RegistryMixin
                        registry = self.get_registry()
                        other_plugin = registry.get_plugin('other')

                        print(args.printable)


For more info on all the tools the toolbox framework provides check the complete documentation!

* Free software: ISC license
* Documentation: https://tool-box.readthedocs.org.

Features
--------

* Integrate your own shell scripts etc. with a single command
* Easily integrate your existing python tools with toolbox by wrapping them in ToolboxPlugin class
* Add persisted configuration to your tools
* Use other tools within your own tools
* search tools in the toolbox
* install other tools from PyPI/github with the toolbox commandline



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
