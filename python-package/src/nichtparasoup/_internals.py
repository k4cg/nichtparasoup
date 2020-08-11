"""Yes, everything is underscored.
Its internal foo that is not for public use.
"""

__all__ = ["_LINEBREAK", '_LOGGER', '_log', '_logging_init', '_message', '_message_exception', '_type_module_name_str']

import logging
import sys
from typing import Any, List, Optional, TextIO, Type, Union

if sys.version_info >= (3, 8):
    from typing import Literal  # pylint: disable=no-name-in-module
else:
    from typing_extensions import Literal

try:
    from termcolor import colored
except ImportError:
    colored = None  # type: ignore

_LINEBREAK = '\r\n'

_LOGGER = logging.getLogger('nichtparasoup')
_LOG_LEVEL_DEFAULT = logging.ERROR

_LOG_LEVEL = Literal['debug', 'info', 'warning', 'error', 'critical']


def _format(message: Union[str, List[str]], color: Optional[str] = None) -> str:
    if isinstance(message, list):
        message = _LINEBREAK.join(message)
    if color and colored:
        message = colored(message, color=color)
    return message.rstrip()


def _logging_init(level: int = _LOG_LEVEL_DEFAULT) -> None:
    if _LOGGER.level == logging.NOTSET:
        _LOGGER.setLevel(level)
    if not logging.root.handlers:
        logging.root.addHandler(logging.StreamHandler())
        logging.root.setLevel(_LOGGER.level)


def _log(level: _LOG_LEVEL, message: Union[str, List[str]], *args: Any, **kwargs: Any) -> None:
    _logging_init()
    message = _format(message)
    getattr(_LOGGER, level)(message, *args, **kwargs)


def _message(message: Union[str, List[str]], color: Optional[str] = None, file: Optional[TextIO] = None) -> None:
    if not file:
        file = sys.stdout
    message = _format(message, color)
    file.write(message + _LINEBREAK)


def _message_exception(exception: BaseException, file: Optional[TextIO] = None) -> None:
    if not file:
        file = sys.stderr
    exception_name = type(exception).__name__
    if colored:
        color = 'yellow' if isinstance(exception, Warning) else 'red'
        exception_name = colored(exception_name, color)
    _message(f'{exception_name}: {exception}', file=file)


def _type_module_name_str(type_: Type[Any]) -> str:
    return f'{type_.__module__}:{type_.__name__}'
