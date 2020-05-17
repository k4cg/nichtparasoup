__all__ = ['main', 'cli']

from logging import Formatter
from typing import Optional

from click import Argument, Command, FloatRange, IntRange, Option, Path, echo, get_terminal_size, style
from click.exceptions import ClickException

from ..config import Config, parse_yaml_file
from ..imagecrawler import BaseImageCrawler
from ..testing.config import (
    PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT, ConfigProbeCallback, ConfigProbeCallbackReason, ConfigProbeResults,
    ConfigTest,
)
from ._internals import _cli_option_debug

_FilePath = str


def main(file: _FilePath, *,
         probe: bool = True, probe_retries: int = PROBE_RETRIES_DEFAULT, probe_delay: float = PROBE_DELAY_DEFAULT,
         probe_fail_fast: bool = False,
         verbose: bool = False
         ) -> None:  # pragma: no cover
    verbose and echo('* VALIDATING...')  # type: ignore
    try:
        config = parse_yaml_file(file)
    except Exception as ex:
        raise ClickException(f'ValidateError: {ex}') from ex
    verbose and echo(f'Config: {config!r}')    # type: ignore
    check_config(config)
    if probe:
        verbose and echo('* PROBING...')  # type: ignore
        probe_config(config, retries=probe_retries, delay=probe_delay, fail_fast=probe_fail_fast, verbose=verbose)


def check_config(config: Config) -> None:  # pragma: no cover
    try:
        ConfigTest().check_duplicates(config)
    except Exception as ex:
        raise ClickException(f'ValidateError: {ex}') from ex


def make_probe_status_callback(*, fail_fast: bool = False, verbose: bool = False) -> ConfigProbeCallback:
    def probe_status_callback(reason: ConfigProbeCallbackReason, imagecrawler: BaseImageCrawler,
                              _: Optional[BaseException]) -> Optional[bool]:
        if reason is ConfigProbeCallbackReason.failure:
            verbose and echo(style('x FAILED', fg='red'), nl=True)  # type: ignore
            return not fail_fast  # stop all the other tests if ``failfast``
        elif reason is ConfigProbeCallbackReason.finish:
            verbose and echo(style('. PASSED', fg='green'), nl=True)  # type: ignore
        elif reason is ConfigProbeCallbackReason.retry:
            verbose and echo(style('r', fg='yellow'), nl=False)  # type: ignore
            return True  # continue with retry
        else:
            verbose and echo(f'{imagecrawler} ', nl=False)  # type: ignore
        return None

    return probe_status_callback


def probe_config(config: Config, *,
                 retries: int, delay: float,
                 fail_fast: bool = False,
                 verbose: bool = False) -> None:  # pragma: no cover
    config_probe_results = ConfigTest().probe(
        config, delay=delay, retries=retries,
        callback=make_probe_status_callback(fail_fast=fail_fast, verbose=verbose))
    verbose and print_probe_errors(config_probe_results)  # type: ignore
    errors = [ic_res for ic_res in config_probe_results if ic_res.result.is_failure]
    if any(errors):
        raise ClickException('ProbeError(s) occurred for:\n\t' + '\n\t'.join(
            str(error.imagecrawler) for error in errors))


def print_probe_errors(probe_results: ConfigProbeResults) -> None:  # pragma: no cover
    echo()
    formatter = Formatter()
    term_width = get_terminal_size()[0]
    printed_errors = False
    for ic_res in probe_results:
        for ec, error in enumerate(ic_res.result.errors):
            echo(f' {ic_res.imagecrawler} '.center(term_width, '-' if ec > 0 else '='), err=True)
            echo(formatter.formatException((type(error), error, error.__traceback__)), err=True)
            echo(style(str(error), fg='red'), err=True)
            printed_errors = True
    printed_errors and echo('=' * term_width, err=True)  # type: ignore


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
        ),
        Option(
            param_decls=['--verbose'],
            help='Enable more output.',
            is_flag=True,
        ),
        _cli_option_debug,
    ]
)

if __name__ == '__main__':
    cli.main()
