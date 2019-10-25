import unittest
from os.path import dirname, join as path_join

from nichtparasoup.config import validate_yaml_file


class ConfigTest(unittest.TestCase):

    def test_validate_yaml_file(self) -> None:
        """ validate the defaults (again) - this file is supposed to be correct """
        # arrange
        file = path_join(dirname(__file__), '..', '..', 'nichtparasoup', 'config', 'default.yaml')
        # act
        valid = validate_yaml_file(file)
        # assert
        self.assertTrue(valid)

    def write_test(self) -> None:
        # TODO: write tests
        self.skipTest('TODO: write the test')
