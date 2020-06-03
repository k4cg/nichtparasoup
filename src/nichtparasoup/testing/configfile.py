__all__ = ["ConfigFileTest"]

from ..config import parse_yaml_file
from .config import ConfigTest

_FilePath = str


class ConfigFileTest:

    def __init__(self, config_file: _FilePath) -> None:  # pragma: no cover
        self.config_file = config_file

    def check_file(self) -> None:  # pragma: no cover
        """Do all necessary tests a file might need.
        """
        config = parse_yaml_file(self.config_file)
        tester = ConfigTest(config)
        tester.check_duplicates()
        tester.probe()
