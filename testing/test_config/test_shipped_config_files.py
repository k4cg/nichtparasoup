import unittest
from glob import glob
from itertools import chain as iter_chain
from os.path import dirname, join as path_join, realpath
from typing import List

from yamale import YamaleTestCase  # type: ignore

from nichtparasoup.config import _defaults_file as config_defaults_file, get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ParseShippedConfigFilesTest(YamaleTestCase):  # type: ignore

    def setUp(self) -> None:
        self.base_dir = realpath(path_join(dirname(__file__), "..", ".."))
        self.schema = path_join("nichtparasoup", "config", 'schema.yaml')
        self.yaml = []  # type: List[str]  # override this in your test

    def tearDown(self) -> None:
        del self.base_dir
        del self.schema
        del self.yaml

    def test_default(self) -> None:
        # arrange
        self.yaml = [config_defaults_file]
        # act & assert
        self.assertTrue(self.validate())

    def test_examples(self) -> None:
        # arrange
        self.yaml = [path_join("examples", "*.yml"), path_join("examples", '**', "*.yml"),
                     path_join("examples", "*.yaml"), path_join("examples", '**', "*.yaml")]
        # act & assert
        self.assertTrue(self.validate())


class ConfigParserDefaultsTest(unittest.TestCase):

    def validate(self, file: str) -> None:
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertIsInstance(config, dict, file)
        for crawler_config in config['crawlers']:
            self.assertIsInstance(get_imagecrawler(crawler_config), BaseImageCrawler, file)

    def test_defaults(self) -> None:
        # arrange
        file = config_defaults_file
        # act & assert
        self.validate(file)

    def test_examples(self) -> None:
        # arrange
        examples_base = realpath(path_join(dirname(__file__), "..", "..", 'examples'))
        files_glob = [path_join(examples_base, '*.yml'), path_join(examples_base, '**', '*.yml'),
                      path_join(examples_base, '*.yaml'), path_join(examples_base, '**', '*.yaml')]
        files = iter_chain(*map(glob, files_glob))  # type: ignore
        # act & assert
        for file in files:
            self.validate(file)  # type: ignore
