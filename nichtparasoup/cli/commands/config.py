__all__ = ["ConfigCommand"]

from os.path import abspath, isfile
from typing import Any, Dict

from nichtparasoup._internals import _confirm, _message, _message_exception
from nichtparasoup.cli.commands import BaseCommand
from nichtparasoup.config import dump_defaults
from nichtparasoup.testing.config import ConfigFileTest


class ConfigCommand(BaseCommand):

    def main(self, options: Dict[str, Any]) -> int:
        active_actions = {k: v for k, v in options.items() if v}  # type: Dict[str, Any]
        if len(active_actions) != 1:
            _message_exception(ValueError('exactly one action required'))
            return 255
        action_name, action_value = active_actions.popitem()
        action = getattr(self, 'run_{}'.format(action_name))
        return action(action_value)  # type: ignore

    @staticmethod
    def run_dump(config_file: str) -> int:
        config_file = abspath(config_file)
        if isfile(config_file):
            overwrite = _confirm('File already exists, overwrite?')
            if overwrite is not True:
                _message('Abort.')
                return 1
        try:
            dump_defaults(config_file)
            return 0
        except Exception as e:
            _message_exception(e)
            return 255

    @staticmethod
    def run_check(config_file: str) -> int:
        config_file = abspath(config_file)
        config_test = ConfigFileTest()
        try:
            config_test.validate(config_file)
            config_test.probe(config_file)
        except Exception as e:
            _message_exception(e)
            return 255
        return 0
