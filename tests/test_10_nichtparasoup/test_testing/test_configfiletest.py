import unittest
from os import path

from nichtparasoup.testing.config import ConfigFileTest


class ConfigFileValidateTest(unittest.TestCase):

    _TESTDATA_DIR = path.join(path.dirname(__file__), 'testdata_configfiletest')

    def test_propagate_errors(self) -> None:
        # nothing to test, yet.
        # calls already covered functions only
        pass

    def test_detect_duplicates(self) -> None:
        import re  # isort:skip
        # arrange
        tester = ConfigFileTest()
        test_file = path.join(self._TESTDATA_DIR, 'duplicates.yaml')
        # act & assert
        with self.assertRaisesRegex(Exception, re.compile(r'duplicate ImageCrawler', re.IGNORECASE)):
            tester.validate(test_file)


class ConfigFileProbeTest(unittest.TestCase):

    def test_propagate_errors(self) -> None:
        # nothing to test, yet.
        # calls already covered functions only
        pass
