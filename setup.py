__author__ = 'jeff'
from setuptools import setup, find_packages

__VERSION__ = (0, 2, 0)

setup(
    name='toolbox',
    version=".".join([str(part) for part in __VERSION__]),
    url='http://github.com/jeff-99/toolbox',
    license='MIT',
    author='Jeff Slort',
    install_requires=['terminaltables'],
    author_email='j_slort@hotmail.com',
    description='Pluggable toolbox',
    long_description="",
    packages=find_packages(),
    entry_points = {'console_scripts': ['tbox = toolbox.cli:main']},
)