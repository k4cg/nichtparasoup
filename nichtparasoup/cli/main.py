__all__ = ['main']

from typing import Any, Callable, Dict

from nichtparasoup.cli.commands.completion import autocomplete, run_command as completion
from nichtparasoup.cli.parser import create_parser
from nichtparasoup.commands.imagecrawler_desc import run_command as imagecrawler_desc
from nichtparasoup.commands.imagecrawler_list import run_command as imagecrawler_list
from nichtparasoup.commands.server_config_check import run_command as server_config_check
from nichtparasoup.commands.server_config_defaults_dump import run_command as server_config_defaults_dump
from nichtparasoup.commands.server_run import run_command as server_run

_COMMANDS = dict(
    server_run=server_run,
    server_config_check=server_config_check,
    server_config_dump_defaults=server_config_defaults_dump,
    imagecrawler_list=imagecrawler_list,
    imagecrawler_desc=imagecrawler_desc,
    completion=completion,
)  # type: Dict[str, Callable[..., int]]


def main() -> int:  # pragma: no cover
    parser = create_parser()
    autocomplete(parser, always_complete_options='long')
    options = parser.parse_args().__dict__  # type: Dict[str, Any]
    command = options.pop('_command')  # type: str
    return _COMMANDS[command](**options)
