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
        config_probe_results = tester.probe()
        failed_imagecrawlers = [
            probed.imagecrawler
            for probed
            in config_probe_results  # pylint: disable=not-an-iterable
            if probed.result.is_failure
        ]
        if failed_imagecrawlers:
            raise Exception('ProbeError(s) occurred for:\n\t' + '\n\t'.join(map(str, failed_imagecrawlers)))
