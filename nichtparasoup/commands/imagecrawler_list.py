__all__ = ['main', 'cli']

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR

from click import Command, Option

from nichtparasoup._internals import _log, _logging_init, _message, _message_exception
from nichtparasoup.imagecrawler import get_imagecrawlers


def main(*, debug: bool = False) -> None:  # pragma: no cover
    _logging_init(L_DEBUG if debug else L_ERROR)
    imagecrawlers = get_imagecrawlers()  # may trigger debug output
    _log('debug', '- List of loaded ImageCrawlers -')
    if len(imagecrawlers) > 0:
        _message(sorted(imagecrawlers.names()))
    else:
        _message_exception(Warning('no ImageCrawler found.'))


cli = Command(
    name='imagecrawler-list',
    help='List available imagecrawlers.',
    callback=main,
    params=[
        Option(
            param_decls=['--debug'],
            help='Enable debug output.',
            is_flag=True,
        ),
    ]
)

if __name__ == '__main__':
    cli.main()  # pylint: disable=no-value-for-parameter
