__all__ = ["BaseCommand", "create_command"]

import importlib
from abc import ABC, abstractmethod
from collections import namedtuple
from types import ModuleType
from typing import Any, Dict, Type


class BaseCommand(ABC):

    @abstractmethod
    def main(self, options: Dict[str, Any]) -> int:  # pragma: no cover
        raise NotImplementedError()


__THIS_PACKAGE = 'nichtparasoup.cli.commands'

_Command = namedtuple('_Command', 'module_name, class_name')

_COMMANDS = dict(
    run=_Command('.run', 'RunCommand'),
    config=_Command('.config', 'ConfigCommand'),
    info=_Command('.info', 'InfoCommand'),
    completion=_Command('.completion', 'CompletionCommand'),
)  # type: Dict[str, _Command]


def create_command(command_name: str) -> BaseCommand:
    command = _COMMANDS[command_name]
    module = importlib.import_module(command.module_name, package=__THIS_PACKAGE)  # type: ModuleType
    command_class = getattr(module, command.class_name)  # type: Type[BaseCommand]
    # No check if ABS is resolved here. In fact this is done via UnitTests.
    return command_class()
