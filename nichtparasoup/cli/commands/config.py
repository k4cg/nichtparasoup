__all__ = ["ConfigCommand"]

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from os.path import abspath, isfile
from typing import Any, Dict

from nichtparasoup._internals import _confirm, _log, _logging_init, _message, _message_exception
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

    def run_dump(self, config_file: str) -> int:
        _logging_init(L_DEBUG if self._debug else L_ERROR)
        config_file = abspath(config_file)
        _log('debug', 'ConfigFile: {}'.format(config_file))
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

    def run_check(self, config_file: str) -> int:
        _logging_init(L_DEBUG if self._debug else L_ERROR)
        config_file = abspath(config_file)
        _log('debug', 'ConfigFile: {}'.format(config_file))
        config_test = ConfigFileTest()
        try:
            config_test.validate(config_file)
            config_test.probe(config_file)
        except Exception as e:
            _message_exception(e)
            return 255
        return 0
