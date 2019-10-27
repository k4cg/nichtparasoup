from os.path import dirname, join as path_join, realpath
from typing import List

from yamale import YamaleTestCase  # type: ignore

from nichtparasoup.config import _defaults_file as config_defaults_file


class ShippedConfigFilesTest(YamaleTestCase):  # type: ignore

    def setUp(self) -> None:
        self.base_dir = realpath(path_join(dirname(__file__), "..", ".."))
        self.schema = path_join("nichtparasoup", "config", 'schema.yaml')
        self.yaml = []  # type: List[str]  # override this in your test

    def tearDown(self) -> None:
        del self.base_dir
        del self.schema
        del self.yaml

    def test_default(self) -> None:
        self.yaml = [config_defaults_file]
        self.assertTrue(self.validate())

    def test_examples(self) -> None:
        self.yaml = [path_join("examples", "*.yaml")]
        self.assertTrue(self.validate())
