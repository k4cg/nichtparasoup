__all__ = ["ConfigFileTest", "ConfigFileTestError"]

from ..config import ConfigFilePath, parse_yaml_file
from .config import ConfigTest


class ConfigFileTest:

    def __init__(self, config_file: ConfigFilePath) -> None:
        self.config_file = config_file

    def check_file(self) -> None:
        """Do all necessary tests a file might need.
        """
        config = parse_yaml_file(self.config_file)
        tester = ConfigTest(config)
        tester.check_duplicates()
        config_probe_results = tester.probe()
        failed = [
            probed
            for probed
            in config_probe_results
            if probed.result.is_failure
        ]
        if failed:
            raise ConfigFileTestError('ProbeError(s) occurred for:\n\t' + '\n\t'.join(
                f'{fail.imagecrawler!r} with {fail.result.errors!r}' for fail in failed
            ))


class ConfigFileTestError(Exception):
    pass
