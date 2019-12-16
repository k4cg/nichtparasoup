from glob import glob
from os.path import dirname, join as path_join, realpath

from nichtparasoup.testing.config import ConfigFilesTest


class ShippedExampleConfigFilesTest(ConfigFilesTest):

    def test_examples(self) -> None:
        files = glob(path_join(dirname(__file__), '..', '..', '..', 'examples', 'config', '*.*'))
        self.assertGreater(len(files), 0)
        for file in files:
            self.validate(realpath(file))
