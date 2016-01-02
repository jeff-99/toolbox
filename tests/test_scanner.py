import unittest
from toolbox.scanner import find_modules, find_contrib_modules, find_local_modules
import os

CONTRIB_MODULES = sorted(['checksum', 'config', 'create', 'install', 'list', 'logs'])
CONTRIB_MODULES_IMPORT = ["toolbox.contrib.{}".format(i) for i in CONTRIB_MODULES]

class TestScanner(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_contrib_modules(self):
        modules = find_contrib_modules()

        self.assertEqual(sorted(modules), CONTRIB_MODULES_IMPORT)

    def test_find_local_modules(self):
        import toolbox.contrib
        module_dir = os.path.dirname(toolbox.contrib.__file__)

        modules = find_local_modules(module_dir)

        self.assertEqual(sorted(modules), CONTRIB_MODULES)




