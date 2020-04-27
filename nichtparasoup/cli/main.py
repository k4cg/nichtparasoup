__all__ = ['cli']

from os.path import dirname, join
from sys import version_info
from typing import Any

from click import Context, Group, Option, echo

from .. import __version__ as nichtparasoup_version
from ..commands.imagecrawler_desc import cli as imagecrawler_desc
from ..commands.imagecrawler_list import cli as imagecrawler_list
from ..commands.server_config_check import cli as server_config_check
from ..commands.server_config_dump_defaults import cli as server_config_dump_defaults
from ..commands.server_run import cli as server_run

# from .completion import cli as completion  # @FIXME removed until fixed -- see module itself


def _cli_print_version(ctx: Context, _: Any, value: Any) -> None:  # pragma: no cover
    if not value or ctx.resilient_parsing:
        return
    echo('{version} from {location} (python {py_version})'.format(
        version=nichtparasoup_version,
        location=join(dirname(__file__), '..'),
        py_version='{}.{}'.format(version_info.major, version_info.minor)
    ))
    ctx.exit()


cli = Group(
    help='Nichtparasoup -- hackspace entertainment system',
    params=[
        Option(
            param_decls=['--version'],
            help='Show the version and exit.',
            callback=_cli_print_version,
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
