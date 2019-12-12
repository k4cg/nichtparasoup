
from nichtparasoup.config import _defaults_file
from nichtparasoup.testing.config import ConfigFilesTest


class DefaultConfigFileTest(ConfigFilesTest):

    def test_examples(self) -> None:
        self.validate(_defaults_file)
