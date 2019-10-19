from time import strftime
from typing import Any, Optional

_logger = None


# TODO: question - do we need multiple log pipelines, one for each cause?
# TODO: question - do we need coloring per cause?
# IDEA: message = "[{colored:cause} ]{time}{reset-color:message}" - coors are random unique and persist per cause


def _logger_date_time_string() -> str:
    return strftime("[%d/%m/%Y %H:%M:%S]")


def _log(type: str, message: str, cause: Optional[Any] = None, *args: Any, **kwargs: Any) -> None:
    global _logger
    if _logger is None:
        import logging
        _logger = logging.getLogger('nichtparasoup')
        if not logging.root.handlers and _logger.level == logging.NOTSET:
            _logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            _logger.addHandler(handler)
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)
