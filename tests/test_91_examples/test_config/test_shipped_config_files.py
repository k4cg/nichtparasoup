import unittest
from glob import glob
from os.path import basename, dirname, join as path_join, realpath

import pytest  # type: ignore
from ddt import ddt, idata, unpack  # type: ignore

from nichtparasoup.config import parse_yaml_file
from nichtparasoup.testing.config import ConfigTest


@ddt
class ShippedExampleConfigFileTest(unittest.TestCase):
    __EXAMPLE_DIR = path_join(dirname(__file__), '..', '..', '..', 'examples', 'config')
    __EXAMPLE_FILES = glob(path_join(__EXAMPLE_DIR, '*.*'), recursive=False)

    def test_has_examples(self) -> None:
        self.assertGreater(len(self.__EXAMPLE_FILES), 0)

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    @idata((basename(file),) for file in __EXAMPLE_FILES)  # type: ignore
    @unpack  # type: ignore
    def test_example(self, filename: str) -> None:
        file = realpath(path_join(self.__EXAMPLE_DIR, filename))
        config = parse_yaml_file(file)
        tester = ConfigTest()
        tester.check_duplicates(config)
        tester.probe(config)
