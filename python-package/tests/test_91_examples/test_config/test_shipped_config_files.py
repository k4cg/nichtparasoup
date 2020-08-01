from glob import glob
from os.path import basename, dirname, join

import pytest

from nichtparasoup.testing.configfile import ConfigFileTest


@pytest.mark.no_cover
class TestShippedExampleConfigFile:
    __EXAMPLE_DIR = join(dirname(__file__), '..', '..', '..', 'examples', 'config')
    __EXAMPLE_FILES = glob(join(__EXAMPLE_DIR, '*.*'), recursive=False)

    def test_has_examples(self) -> None:
        assert len(self.__EXAMPLE_FILES) > 0

    @pytest.mark.online  # probing goes over the internet
    @pytest.mark.slow  # probing might be slow
    @pytest.mark.parametrize('file', __EXAMPLE_FILES, ids=basename)
    def test_example(self, file: str) -> None:
        ConfigFileTest(file).check_file()
