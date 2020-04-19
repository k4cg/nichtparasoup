__all__ = ['cli']

from os.path import dirname
from sys import version_info
from typing import Any

from click import Context, Group, Option, echo

import nichtparasoup
# from nichtparasoup.cli.completion import main as completion # @FIXME removed until fixed -- see module itself
from nichtparasoup.commands.imagecrawler_desc import cli as imagecrawler_desc
from nichtparasoup.commands.imagecrawler_list import cli as imagecrawler_list
from nichtparasoup.commands.server_config_check import cli as server_config_check
from nichtparasoup.commands.server_config_dump_defaults import cli as server_config_dump_defaults
from nichtparasoup.commands.server_run import cli as server_run


def _print_version(ctx: Context, _: Any, value: Any) -> None:
    if not value or ctx.resilient_parsing:
        return
    echo('{version} from {location} (python {py_version})'.format(
        version=nichtparasoup.__version__,
        location=dirname(nichtparasoup.__file__),
        py_version='{}.{}'.format(version_info.major, version_info.minor)
    ))
    ctx.exit()


cli = Group(
    help='Nichtparasoup -- hackspace entertainment system',
    params=[
        Option(
            param_decls=['--version'],
            help='Show the version and exit.',
            callback=_print_version,
            is_flag=True,
            expose_value=False,
            is_eager=True,
        ),
    ],
    commands={
        'server': Group(
            help='Manage server.',
            commands={
                'run': server_run,
                'config': Group(
                    help='Manage server configs.',
                    commands={
                        'check': server_config_check,
                        'dump-defaults': server_config_dump_defaults,
                    }
                ),
            }
        ),
        'imagecrawler': Group(
            help='Manage imagecrawlers.',
            commands={
                'list': imagecrawler_list,
                'desc': imagecrawler_desc,
            }
        ),
        # 'completion': completion,  # @FIXME removed until fixed -- see module itself
    }
)
