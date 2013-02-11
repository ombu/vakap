import sys
sys.path.append('..')

import unittest
from vakap import vakap
from helpers import capture


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class YamlConfigTest(unittest.TestCase):

    def setUp(self):
        self.options = AttributeDict({'config': 'tests/config.yaml'})

    def testConfig(self):
        sites = vakap.parse_config(self.options)
        self.assertEqual(2, len(sites))

    def testList(self):
        out = capture()(vakap.run)(self.options, ['list'])
        expect = ['foo', '-', 'TgzComponent', 'bar', '-', 'TgzComponent']
        self.assertEquals(expect, out[:6])

    def testHosts(self):
        self.assertRaises(
            NotImplementedError, vakap.run, self.options, ['hosts'])

if __name__ == '__main__':
    unittest.main()
