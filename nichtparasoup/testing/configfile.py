__all__ = ["ConfigFileTest"]

from ..config import parse_yaml_file
from .config import ConfigTest

_FilePath = str


class ConfigFileTest:

    @staticmethod
    def check_file(file: _FilePath) -> None:  # pragma: no cover
        """Do all necessary tests a file might need.
        """
        config = parse_yaml_file(file)
        tester = ConfigTest()
        tester.check_duplicates(config)
        tester.probe(config)
