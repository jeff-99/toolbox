=====
Usage
=====

Install a Tool
----

To install a plugin and register it to the toolbox you can run::

    tbox install [--external] tool
This searches the current working directory for a match , if it can't find it will install it from PyPI or git using pip
If you already have a toolbox tool installed and want to register it to the toolbox just add the external flag

Use a Tool
----

Using a tool is really simple every installed tool will be available as a subcommand of the toolbox.
To use the 'example' tool you execute::

    tbox example



======
Custom Tools
=====

Register a shell command
----

already have an awesome script or just want to alias a complex command run the following::

    tbox create -t shell -i example
This will create a new Toolbox tool named example and install it afer asking some basic questions.


Create a new Tool
----
To use the Toolbox we need a Tool. Let's create one::

    tbox create example
This sets up the current working directory with an simple template of a basic Tool.

Install the newly created tool as a dev tool by::

    tbox install --dev ./example

To check if this worked check if your new tool is listed::

    tbox list


Customizing
----
Our new tool is not very usefull yet, but that's about to change!
An tool should always subclass the toolbox.plugin.ToolboxPlugin . Which essentially means it needs to implement an prepare_parser and execute method.
the prepare parser get an instance of an argparse.ArgumentParser. This method sets up the tool for usage on the commandline

the execute method is the main entry point for the commandline and should accept an argparse Namespace.


Adding to the Mix
----

The toolbox.mixin module provides some usefull mixins to extend the new custom Tool with basic functionality
For example by adding the ConfigMixin to the new tool class the tool gets access to a special plugin dictionary that is persisted between usages.

Tools can use other tools by adding the RegistryMixin which provides access to the toolbox registry from wich other tools can be loaded.

There is also an LogMixin to provide a no-config python logging logger instance.
