__all__ = ['LOGNAME', 'LOGDIR']

import logging
import os
from pathlib import Path
from shutil import rmtree

from nichtparasoup._internals import _LOGGER
from nichtparasoup.core.imagecrawler import RemoteFetcher


def _check_name(name: str) -> bool:
    allowed_special = '+-._'
    for char in name:
        if not char.isalnum() and char not in allowed_special:
            return False
    return True


LOGNAME = os.environ.get('NP_TESTLOG_NAME', '').strip()
LOGDIR = Path(__file__).parent / '.logs' / LOGNAME if _check_name(LOGNAME) else None

if LOGDIR:
    if LOGDIR.exists():
        rmtree(LOGDIR)
    LOGDIR.mkdir(parents=True)
    os.environ.setdefault(RemoteFetcher.ENV_STOREDIR, str(LOGDIR))
    _logfile = LOGDIR / 'nichtparasoup.log'
    _LOGGER.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(_logfile)
    file_handler.setFormatter(logging.Formatter(fmt='{asctime} {levelname}: {message}', style='{'))
    _LOGGER.addHandler(file_handler)
    _LOGGER.debug('+++ ENABLED DEBUG FOR TEST LOGS +++')
