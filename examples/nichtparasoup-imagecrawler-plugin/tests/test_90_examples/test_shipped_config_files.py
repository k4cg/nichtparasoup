from glob import glob
from os.path import basename, dirname, join

import pytest

from nichtparasoup.testing.configfile import ConfigFileTest


class TestShippedExampleConfigFile:
    __EXAMPLE_DIR = join(dirname(__file__), '..', '..', 'examples')
    __EXAMPLE_FILES = [basename(f) for f in glob(join(__EXAMPLE_DIR, '*.*'), recursive=False)]

    def test_has_examples(self) -> None:
        assert len(self.__EXAMPLE_FILES) > 0

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    @pytest.mark.parametrize('filename', __EXAMPLE_FILES)  # type: ignore
    def test_example(self, filename: str) -> None:
        file = join(self.__EXAMPLE_DIR, filename)
        ConfigFileTest(file).check_file()
