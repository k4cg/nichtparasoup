__all__ = ['main', 'cli']

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from os.path import isfile
from typing import Optional

from click import Argument, BadParameter, ClickException, Command, Option, Path, confirm

from nichtparasoup._internals import _log, _logging_init
from nichtparasoup.config import dump_defaults


def main(file: str, *, overwrite: Optional[bool] = None, debug: bool = False) -> None:  # pragma: no cover
    _logging_init(L_DEBUG if debug else L_ERROR)
    _log('debug', 'ConfigFile: {}'.format(file))
    if isfile(file):
        if overwrite is None:
            confirm('File already exists, overwrite?', default=False, abort=True)
        elif not overwrite:
            raise BadParameter('File already exists.', param_hint='file')
    _write_file(file)


def _write_file(file: str) -> None:  # pragma: no cover
    try:
        dump_defaults(file)
    except Exception as e:  # pylint: disable=broad-except
        _log('debug', '', exc_info=True)
        raise ClickException(str(e)) from e


cli = Command(
    name='server-config-dump-defaults',
    help='Dump the builtin default YAML config to give a quick start when writing an own config.',
    short_help='Dump the builtin default YAML config.',
    callback=main,
    params=[
        Argument(
            param_decls=['file'],
            type=Path(writable=True, dir_okay=False, resolve_path=True)
        ),
        Option(
            param_decls=['--overwrite/--no-overwrite'],
            help='Control target overwrite. If omitted, confirmation question might appear.',
            default=None,
            show_default=True,
        ),
        Option(
            param_decls=['--debug'],
            help='Enable debug output.',
            is_flag=True,
        ),
    ]
)

if __name__ == '__main__':
    cli.main()
