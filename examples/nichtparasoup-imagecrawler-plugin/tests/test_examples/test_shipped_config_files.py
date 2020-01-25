from glob import glob
from os.path import basename, dirname, join as path_join, realpath

from ddt import ddt, idata, unpack  # type: ignore

from nichtparasoup.testing.config import ConfigFilesTest


@ddt
class ShippedExampleConfigFilesTest(ConfigFilesTest):

    __EXAMPLE_DIR = path_join(dirname(__file__), '..', '..', 'examples')
    __EXAMPLE_FILES = glob(path_join(__EXAMPLE_DIR, '*.*'), recursive=False)

    def test_has_examples(self) -> None:
        self.assertGreater(len(self.__class__.__EXAMPLE_FILES), 0)

    @idata((basename(file),) for file in __EXAMPLE_FILES)  # type: ignore
    @unpack  # type: ignore
    def test_example(self, filename: str) -> None:
        file = realpath(path_join(self.__class__.__EXAMPLE_DIR, filename))
        self.validate(file)
        self.probe(file)
