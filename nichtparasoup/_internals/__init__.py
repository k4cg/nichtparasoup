__all__ = ['_logger', '_log', '_message', '_message_exception', '_confirm']
"""
yes, everything is underscored.
its internal foo that is not for public use.
"""

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

_logger = logging.getLogger('nichtparasoup')

_LOG_LEVEL = Literal['debug', 'info', 'warning', 'error', 'critical', 'log', 'exception']


def _log(level: _LOG_LEVEL, message: str, *args: Any, **kwargs: Any) -> None:
    if not logging.root.handlers and _logger.level == logging.NOTSET:
        _logger.setLevel(logging.INFO)
        _logger.addHandler(logging.StreamHandler())
    getattr(_logger, level)(message.rstrip(), *args, **kwargs)


def _message(message: str, color: Optional[str] = None, file: Optional[TextIO] = None) -> None:
    from sys import stdout
    newline = '\r\n'
    if not file:
        file = stdout
    if color and colored:
        message = colored(message, color=color)
    file.write('{}{}'.format(message.rstrip(), newline))


def _message_exception(exception: BaseException, file: Optional[TextIO] = None) -> None:
    if not file:
        from sys import stderr
        file = stderr
    exception_name = type(exception).__name__
    if colored:
        color = 'yellow' if isinstance(exception, Warning) else 'red'
        exception_name = colored(exception_name, color)
    _message('{}: {}'.format(exception_name, exception), file=file)


def _confirm(prompt: str, default: bool = False) -> Optional[bool]:
    rv = {
        'y': True,
        'yes': True,
        '': default,
        'n': False,
        'no': False,
    }
    options = 'Y/n' if default else 'y/N'
    try:
        value = input('{!s} [{}]: '.format(prompt, options)).lower().strip()
        return rv[value]
    except (KeyboardInterrupt, EOFError, KeyError):
        return None
