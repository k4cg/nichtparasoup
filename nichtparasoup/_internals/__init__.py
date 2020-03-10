"""Yes, everything is underscored.
Its internal foo that is not for public use.
"""

__all__ = ['_LOGGER', '_log', '_logging_init', '_message', '_message_exception', '_confirm']

import logging
import sys
from typing import Any, Optional, TextIO

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

try:
    from termcolor import colored
except ImportError:
    colored = None  # type: ignore

_LOGGER = logging.getLogger('nichtparasoup')

_LOG_LEVEL = Literal['debug', 'info', 'warning', 'error', 'critical', 'log', 'exception']


def _log(level: _LOG_LEVEL, message: str, *args: Any, **kwargs: Any) -> None:
    if not logging.root.handlers and _LOGGER.level == logging.NOTSET:
        _LOGGER.setLevel(logging.INFO)
        _LOGGER.addHandler(logging.StreamHandler())
    getattr(_LOGGER, level)(message.rstrip(), *args, **kwargs)


def _logging_init(level: int) -> None:  # pragma: no cover
    if not logging.root.handlers:
        logging.root.setLevel(level)
        logging.root.addHandler(logging.StreamHandler())


def _message(message: str, color: Optional[str] = None, file: Optional[TextIO] = None) -> None:
    newline = '\r\n'
    if not file:
        file = sys.stdout
    if color and colored:
        message = colored(message, color=color)
    file.write('{}{}'.format(message.rstrip(), newline))


def _message_exception(exception: BaseException, file: Optional[TextIO] = None) -> None:
    if not file:
        file = sys.stderr
    exception_name = type(exception).__name__
    if colored:
        color = 'yellow' if isinstance(exception, Warning) else 'red'
        exception_name = colored(exception_name, color)
    _message('{}: {}'.format(exception_name, exception), file=file)


def _confirm(prompt: str, default: bool = False) -> Optional[bool]:
    return_values = {
        'y': True,
        'yes': True,
        '': default,
        'n': False,
        'no': False,
    }
    options = 'Y/n' if default else 'y/N'
    try:
        value = input('{!s} [{}]: '.format(prompt, options)).lower().strip()
        return return_values[value]
    except (KeyboardInterrupt, EOFError, KeyError):
        return None
