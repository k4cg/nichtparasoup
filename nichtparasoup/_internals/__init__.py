__all__ = ['_logger', '_log', '_message', '_message_exception']
"""
yes, everything is underscored.
its internal foo that is not for public use.
"""

import logging
from typing import Any, Optional, TextIO

try:
    from termcolor import colored
except ImportError:
    colored = None  # type: ignore

_logger = logging.getLogger('nichtparasoup')


def _log(type: str, message: str, *args: Any, **kwargs: Any) -> None:
    if not logging.root.handlers and _logger.level == logging.NOTSET:
        _logger.setLevel(logging.INFO)
        _logger.addHandler(logging.StreamHandler())
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)


def _message(message: str, color: Optional[str] = None, file: Optional[TextIO] = None) -> None:
    from sys import stdout
    newline = '\r\n'
    if not file:
        file = stdout
    if color and colored:
        message = colored(message, color=color)
    file.write('{}{}'.format(message, newline))


def _message_exception(exception: BaseException, file: Optional[TextIO] = None) -> None:
    if not file:
        from sys import stderr
        file = stderr
    exception_name = type(exception).__name__
    if colored:
        color = 'yellow' if isinstance(exception, Warning) else 'red'
        exception_name = colored(exception_name, color, 'on_grey')

    _message('{}: {}'.format(exception_name, exception), file=file)
