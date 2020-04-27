__all__ = ['main', 'cli']

from typing import Optional

from click import Argument, Command, FloatRange, IntRange, Option, Path, echo
from click.exceptions import ClickException

from .._internals import _log
from ..config import Config
from ..imagecrawler import BaseImageCrawler
from ..testing.config import PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT, ConfigFileTest, ConfigTest, ProbeCallbackReason


def main(file: str, *,
         probe: bool = True, probe_retries: int = PROBE_RETRIES_DEFAULT, probe_delay: float = PROBE_DELAY_DEFAULT,
         probe_fail_fast: bool = False,
         ) -> None:  # pragma: no cover
    verbose = False  # TODO
    _log('debug', '* VALIDATING...')
    config = _validate_file(file)
    _log('debug', 'Config: {}'.format(config))
    if probe:
        _log('debug', '* PROBING...')
        _probe_config(config, retries=probe_retries, delay=probe_delay, fail_fast=probe_fail_fast, verbose=verbose)


def _validate_file(file: str) -> Config:  # pragma: no cover
    try:
        return ConfigFileTest().validate(file)
    except Exception as e:
        raise ClickException('ValidateError: {!s}'.format(e)) from e


def _echo_probe_status(reason: ProbeCallbackReason, imagecrawler: BaseImageCrawler, _: Optional[Exception]) -> None:
    if reason is ProbeCallbackReason.failure:
        echo(' FAILED', nl=True)
    elif reason is ProbeCallbackReason.finish:
        echo(' PASSED', nl=True)
    elif reason is ProbeCallbackReason.retry:
        echo('.', nl=False)
    else:
        echo('{!r} '.format(imagecrawler), nl=False)


def _probe_config(config: Config, *,
                  retries: int, delay: float,
                  fail_fast: bool = False,
                  verbose: bool = False) -> None:  # pragma: no cover

    config_test = ConfigTest()
    try:
        config_test.probe(config, delay=delay, retries=retries,
                          fail_fast=fail_fast,
                          callback=_echo_probe_status if verbose else None)
    except Exception as e:
        verbose and echo()  # type: ignore
        raise ClickException('ProbeError: {!s}'.format(e)) from e


cli = Command(
    name='server-config-check',
    help='Validate (and probe) a config file.',
    callback=main,
    params=[
        Argument(
            param_decls=['file'],
            type=Path(exists=True, dir_okay=False, resolve_path=True)
        ),
        Option(
            param_decls=['--probe/--no-probe'],
            help='Enable/disable probe crawls.',
            default=True,
            show_default=True
        ),
        Option(
            param_decls=['--probe-retries'],
            help='Set number of probe retries in case of errors.',
            metavar='retries',
            type=IntRange(min=0),
            default=PROBE_RETRIES_DEFAULT,
            show_default=True,
        ),
        Option(
            param_decls=['--probe-delay'],
            help='Set probe delay in seconds.',
            metavar='seconds',
            type=FloatRange(min=0),
            default=PROBE_DELAY_DEFAULT,
            show_default=True,
        ),

        Option(
            param_decls=['--probe-fail-fast/--probe-no-fail-fast'],
            help='Enable/disable probe fast failing.',
            default=False,
            show_default=True
        )]
)

if __name__ == '__main__':
    cli.main()
