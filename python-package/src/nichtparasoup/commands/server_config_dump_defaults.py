__all__ = ['main', 'cli']

from os.path import isfile
from typing import Optional

from click import Argument, BadParameter, ClickException, Command, Option, Path, confirm

from .._internals import _log
from ..config import ConfigFilePath, dump_defaults
from ._internals import _cli_option_debug


def main(file: ConfigFilePath, *, overwrite: Optional[bool] = None) -> None:
    _log('debug', 'ConfigFile: %r', file)
    if isfile(file):
        if overwrite is None:
            overwrite = confirm(
                'File already exists, overwrite?',
                default=False,
                abort=True
            )
        if not overwrite:
            raise BadParameter('File already exists.', param_hint='file')
    _write_file(file)


def _write_file(file: ConfigFilePath) -> None:
    try:
        dump_defaults(file)
    except Exception as ex:
        _log('debug', 'Handled exception: %s', ex, exc_info=ex)
        raise ClickException(str(ex)) from ex


cli = Command(
    name='server-config-dump-defaults',
    help='Dump the builtin default config to give a quick start when writing an own config.',
    short_help='Dump the builtin default config.',
    callback=main,
    params=[
        Argument(
            param_decls=['file'],
            type=Path(writable=True, dir_okay=False, resolve_path=True)
        ),
        Option(
            param_decls=['--overwrite/--no-overwrite'],
            help='Control target overwrite. If omitted confirmation question might appear.',
            default=None,
            show_default=True,
        ),
        _cli_option_debug,
    ]
)

if __name__ == '__main__':
    try:
        prog_name: Optional[str] = __spec__.name  # type: ignore[name-defined]
    except NameError:
        prog_name = None
    cli.main(prog_name=prog_name)
