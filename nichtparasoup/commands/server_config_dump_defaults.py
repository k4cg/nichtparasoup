__all__ = ['main']

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from os.path import isfile
from typing import Optional

from click import BadParameter, Path, argument, command, confirm, option

from nichtparasoup._internals import _log, _logging_init
from nichtparasoup.config import dump_defaults


@command(name='server-config-dump-defaults')
@argument('file', type=Path(writable=True, dir_okay=False, resolve_path=True))
@option('--overwrite/--no-overwrite', default=None, help='overwrite file target.')
@option('--debug', is_flag=True, help='enable debug output.')
def main(file: str, *, overwrite: Optional[bool] = None, debug: bool = False) -> None:  # pragma: no cover
    """Dump the builtin default YAML.

    The dumped defaults give a quick start when writing an own config.
    """
    _logging_init(L_DEBUG if debug else L_ERROR)
    _log('debug', 'ConfigFile: {}'.format(file))
    if isfile(file):
        if overwrite is None:
            confirm('File already exists, overwrite?', default=False, abort=True)
        elif not overwrite:
            raise BadParameter('File already exists.', param_hint='file')
    dump_defaults(file)


if __name__ == '__main__':
    main()
