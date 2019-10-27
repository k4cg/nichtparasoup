from time import strftime
from typing import Any, List, NoReturn, Optional, TextIO, Union

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


def _exit(status: int = 0,
          message: Optional[Union[str, List[str]]] = None, exception: Optional[Exception] = None,
          file: Optional[TextIO] = None) -> NoReturn:
    import sys
    newline = '\r\n'
    if message:
        if type(message) == list:
            message = newline.join(message)
        (file if file else (sys.stderr if status > 0 else sys.stdout)).write('{0}{eot}'.format(message, eot=newline))
    if exception:
        (file if file else sys.stderr).write('{0.__name__}: {1}{eot}'.format(type(exception), exception, eot=newline))
    sys.exit(status)
