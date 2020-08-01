__all__ = ['main', 'cli']

from enum import Enum, unique
from logging import Formatter
from time import time
from typing import Any, Dict, Optional, Union

from click import Argument, Command, FloatRange, IntRange, Option, Path, echo, get_terminal_size, style, unstyle
from click.exceptions import ClickException

from .._internals import _log
from ..config import Config, parse_yaml_file
from ..imagecrawler import BaseImageCrawler
from ..testing.config import (
    PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT, ConfigProbeCallback, ConfigProbeCallbackReason, ConfigProbeResults,
    ConfigTest,
)
from ._internals import _cli_option_debug

_FilePath = str


def _print_if(condition: Any, *args: Any, **kwargs: Any) -> None:
    if condition:
        echo(*args, **kwargs)


def main(file: _FilePath, *,
         probe: bool = True, probe_retries: int = PROBE_RETRIES_DEFAULT, probe_delay: float = PROBE_DELAY_DEFAULT,
         probe_fail_fast: bool = False,
         verbose: bool = False
         ) -> None:  # pragma: no cover
    _print_if(verbose, '* VALIDATING...')
    try:
        config = parse_yaml_file(file)
    except Exception as ex:
        _log('debug', 'Error during config parse.', exc_info=ex)
        raise ClickException(f'ValidationError: {ex}') from ex
    _print_if(verbose, f'Config: {config!r}')
    check_config(config)
    if probe:
        _print_if(verbose, '* PROBING...')
        probe_config(config, retries=probe_retries, delay=probe_delay, fail_fast=probe_fail_fast, verbose=verbose)


def check_config(config: Config) -> None:  # pragma: no cover
    try:
        ConfigTest(config).check_duplicates()
    except Exception as ex:
        _log('debug', 'Error during config check.', exc_info=ex)
        raise ClickException(f'ValidationError: {ex}') from ex


class _ProbeStatusCallbackBehaviour:
    def __init__(self,
                 return_value: Optional[bool],
                 print_string: str,
                 print_newline: bool
                 ) -> None:  # pragma: no cover
        self.return_value = return_value
        self.print_string = print_string
        self.print_newline = print_newline


_COLOR_SUCCESS = 'green'
_COLOR_WARNING = 'yellow'
_COLOR_FAILURE = 'red'


def make_probe_status_callback(*, fail_fast: bool = False, verbose: bool = False) -> ConfigProbeCallback:
    callback_behaviour: Dict[ConfigProbeCallbackReason, _ProbeStatusCallbackBehaviour] = {
        ConfigProbeCallbackReason.start:
            _ProbeStatusCallbackBehaviour(None, '{imagecrawler} ', False),
        ConfigProbeCallbackReason.retry:
            _ProbeStatusCallbackBehaviour(True, style('r', fg=_COLOR_WARNING), False),
        ConfigProbeCallbackReason.failure:
            _ProbeStatusCallbackBehaviour(not fail_fast, style('x FAILED', fg=_COLOR_FAILURE), True),
        ConfigProbeCallbackReason.finish:
            _ProbeStatusCallbackBehaviour(None, style('. PASSED', fg=_COLOR_SUCCESS), True),
    }

    def callback(reason: ConfigProbeCallbackReason, imagecrawler: BaseImageCrawler,
                 _: Optional[BaseException]) -> Optional[bool]:
        apply = callback_behaviour[reason]
        _print_if(verbose, apply.print_string.format(imagecrawler=imagecrawler), nl=apply.print_newline)
        return apply.return_value

    return callback


def probe_config(config: Config, *,
                 retries: int, delay: float,
                 fail_fast: bool = False,
                 verbose: bool = False) -> None:  # pragma: no cover
    # TODO implement a progress bar ?
    config_probe_start = time()
    config_probe_results = ConfigTest(config).probe(
        delay=delay, retries=retries,
        callback=make_probe_status_callback(fail_fast=fail_fast, verbose=verbose))
    config_probe_end = time()
    if verbose:
        print_probed_erroneous(config_probe_results)
        print_probed_summary(config_probe_results, elapsed_seconds=config_probe_end - config_probe_start)
    failed_imagecrawlers = [
        probed.imagecrawler
        for probed
        in config_probe_results  # pylint: disable=not-an-iterable
        if probed.result.is_failure
    ]
    if failed_imagecrawlers:
        raise ClickException('ProbeError(s) occurred for:\n\t' + '\n\t'.join(map(str, failed_imagecrawlers)))


def print_probed_erroneous(probe_results: ConfigProbeResults) -> None:  # pragma: no cover
    echo()
    ex_formatter = Formatter()
    term_width = get_terminal_size()[0]
    for probed in filter(lambda probed: probed.result.is_erroneous, probe_results):
        error_color = _COLOR_FAILURE if probed.result.is_failure else _COLOR_WARNING
        result_type = 'ERROR' if probed.result.is_failure else 'WARNING'
        for error_num, error in enumerate(probed.result.errors):
            line_delimiter = '-' if error_num > 0 else '='
            echo(style(f' {result_type}: {probed.imagecrawler} '.center(term_width, line_delimiter), fg=error_color),
                 err=True)
            echo(style(str(error), fg=error_color), err=True)
            echo(ex_formatter.formatException((type(error), error, error.__traceback__)), err=True)


@unique
class _ProbedSummaryType(Enum):
    failed = 'failed'
    passed = 'passed'
    warned = 'warned'


class _ProbedSummaryCounter:
    def __init__(self, color: str, value: int = 0) -> None:  # pragma: no cover
        self.color = color
        self.value = value


def print_probed_summary(probe_results: ConfigProbeResults, *,
                         elapsed_seconds: Optional[Union[int, float]]
                         ) -> None:  # pragma: no cover
    summary: Dict[_ProbedSummaryType, _ProbedSummaryCounter] = {
        _ProbedSummaryType.failed: _ProbedSummaryCounter(
            _COLOR_FAILURE,
            len([None for probed in probe_results if probed.result.is_failure])
        ),
        _ProbedSummaryType.passed: _ProbedSummaryCounter(
            _COLOR_SUCCESS,
            len([None for probed in probe_results if not probed.result.is_failure])
        ),
        _ProbedSummaryType.warned: _ProbedSummaryCounter(
            _COLOR_WARNING,
            len([None for probed in probe_results if not probed.result.is_failure and probed.result.is_erroneous])
        ),
    }
    overall_result = _ProbedSummaryType.failed \
        if summary[_ProbedSummaryType.failed].value > 0 \
        else _ProbedSummaryType.passed
    summary_color = summary[overall_result].color
    summary_string_spacer = ' '
    summary_string = summary_string_spacer + ', '.join(
        style(f'{counter.value} {counter_type.value}', fg=counter.color, bold=counter_type == overall_result)
        for counter_type, counter
        in summary.items()
        if counter.value > 0
    ) + summary_string_spacer
    if elapsed_seconds is not None:
        summary_string += style(f'in {elapsed_seconds:.2f}s', fg=summary_color) + summary_string_spacer
    summary_width = len(unstyle(summary_string))
    term_width = get_terminal_size()[0]
    line_width = max(0, term_width - summary_width)
    line_width_first_half = line_width // 2
    echo(''.join([
        style('=' * line_width_first_half, fg=summary_color) if line_width_first_half else '',
        summary_string,
        style('=' * (line_width - line_width_first_half), fg=summary_color) if line_width_first_half else '',
    ]), err=True)


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
    try:
        prog_name: Optional[str] = __spec__.name  # type: ignore[name-defined]
    except NameError:
        prog_name = None
    cli.main(prog_name=prog_name)
