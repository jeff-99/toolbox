#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'terminaltables'
]

test_requirements = [

]

setup(
    name='tool-box',
    version='0.3.0',
    description="tools for your toolbox , neatly organised",
    long_description=readme + '\n\n' + history,
    author='Jeff Slort',
    author_email='j_slort@hotmail.com',
    url='http://github.com/jeff-99/toolbox',
    license='MIT',
    zip_safe=False,
    keywords='toolbox',

    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,

    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'tbox = toolbox.cli:main',
            'toolbox = toolbox.cli:main'
        ]
    },
)
