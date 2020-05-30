"""Yes, everything is underscored.
Its internal foo that is not for public use.
"""

__all__ = ['_cli_option_debug']

# @TODO: write the verbosity option as a counter
# and apply those to the commands ...

import logging
from typing import Any

from click import Context, Option

from .._internals import _LOGGER


def __cli_enable_debug(ctx: Context, _: Any, value: bool) -> None:  # pragma: no cover
    if not value or ctx.resilient_parsing:
        return
    level = logging.DEBUG
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(fmt='{levelname}:{name}: {message}', style='{'))
    logging.root.addHandler(stream_handler)
    logging.root.setLevel(level)
    _LOGGER.setLevel(level)
    _LOGGER.debug(' *** DEBUG ENABLED ***')


_cli_option_debug = Option(
    param_decls=['--debug'],
    help='TODO',
    is_flag=True,
    expose_value=False,
    callback=__cli_enable_debug
)
