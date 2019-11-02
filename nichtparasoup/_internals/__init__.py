__all__ = ['_logger_date_time_string', '_log', '_message', '_exit']
"""
yes, everything is underscored.
its internal foo that is not for public use.
"""

import logging
from typing import NoReturn, Optional, TextIO

try:
    from termcolor import colored
except ImportError:
    colored = None  # type: ignore

_logger = logging.getLogger('nichtparasoup')
_logger.setLevel(logging.INFO)
_logger.addHandler(logging.StreamHandler())


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


def _exit(status: int = 0,
          message: Optional[str] = None, exception: Optional[Exception] = None,
          file: Optional[TextIO] = None) -> NoReturn:
    if not file:
        from sys import stderr
        file = stderr if status > 0 else None
    if message:
        _message(message, file=file)
    if exception:
        _message_exception(exception, file=file)
    from sys import exit
    exit(status)
