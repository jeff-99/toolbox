__author__ = 'jeff'
from setuptools import setup

setup(
    name='toolbox',
    version='0.0.1',
    url='http://github.com/jeff-99/toolbox',
    license='MIT',
    author='Jeff Slort',
    install_requires=['terminaltables'],
    author_email='j_slort@hotmail.com',
    description='Pluggable toolbox',
    long_description="",
    packages=['toolbox','toolbox.contrib'],
    entry_points = {'console_scripts': ['tbox = toolbox.cli:main']},
)