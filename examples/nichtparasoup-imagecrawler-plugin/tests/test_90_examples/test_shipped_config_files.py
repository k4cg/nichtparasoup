import unittest
from glob import glob
from os.path import basename, dirname, join

import pytest  # type: ignore
from ddt import data, ddt  # type: ignore

from nichtparasoup.config import parse_yaml_file
from nichtparasoup.testing.config import ConfigTest


@ddt
class ShippedExampleConfigFileTest(unittest.TestCase):
    __EXAMPLE_DIR = join(dirname(__file__), '..', '..', 'examples')
    __EXAMPLE_FILES = [basename(f) for f in glob(join(__EXAMPLE_DIR, '*.*'), recursive=False)]

    def test_has_examples(self) -> None:
        self.assertGreater(len(self.__EXAMPLE_FILES), 0)

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    @data(*__EXAMPLE_FILES)  # type: ignore
    def test_example(self, filename: str) -> None:
        file = join(self.__EXAMPLE_DIR, filename)
        config = parse_yaml_file(file)
        tester = ConfigTest()
        tester.check_duplicates(config)
        tester.probe(config)
