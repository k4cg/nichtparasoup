__all__ = ['_logger_date_time_string', '_log', '_message', '_exit']
"""
yes, everything is underscored.
its internal foo that is not for public use.
"""

from time import strftime
from typing import Any, NoReturn, Optional, TextIO

try:
    from termcolor import colored
except ImportError:
    colored = None  # type: ignore

__logger = None


# TODO: question - do we need multiple log pipelines, one for each cause?
# TODO: question - do we need coloring per cause?
# IDEA: message = "[{colored:cause} ]{time}{reset-color:message}" - coors are random unique and persist per cause


def _logger_date_time_string() -> str:
    return strftime("[%d/%m/%Y %H:%M:%S]")


def _log(type: str, message: str, cause: Optional[Any] = None, *args: Any, **kwargs: Any) -> None:
    del cause  # currently not used, kept for the future
    global __logger
    if __logger is None:
        import logging
        __logger = logging.getLogger('nichtparasoup')
        if not logging.root.handlers and __logger.level == logging.NOTSET:
            __logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            __logger.addHandler(handler)
    getattr(__logger, type)(message.rstrip(), *args, **kwargs)


def _message(message: str, color: Optional[str] = None, file: Optional[TextIO] = None) -> None:
    from sys import stdout
    newline = '\r\n'
    if not file:
        file = stdout
    if color and colored:
        message = colored(message, color=color)
    file.write('{}{}'.format(message, newline))


def _message_exception(exception: BaseException, debug: bool = True, file: Optional[TextIO] = None) -> None:
    if not file:
        from sys import stderr
        file = stderr
    if debug:
        pass
        # TODO: bring beutiful output
        # from traceback import format_exception
        # x = format_exception(type(exception), exception)
        # _log("error", exception)
    exception_name = type(exception).__name__
    if colored:
        color = 'yellow' if isinstance(exception, Warning) else 'red'
        exception_name = colored(exception_name, color=color)
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
