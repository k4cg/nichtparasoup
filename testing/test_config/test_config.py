import unittest

from nichtparasoup.config import validate_yaml_file

from os.path import join as path_join, dirname


class ConfigTest(unittest.TestCase):

    def test_validate_yaml_file(self):
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
