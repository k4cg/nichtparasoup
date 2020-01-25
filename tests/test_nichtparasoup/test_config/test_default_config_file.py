from nichtparasoup.config import _DEFAULTS_FILE
from nichtparasoup.testing.config import ConfigFilesTest


class DefaultConfigFileTest(ConfigFilesTest):

    def test_examples(self) -> None:
        self.validate(_DEFAULTS_FILE)
        self.probe(_DEFAULTS_FILE)
