__all__ = ['main', 'cli']

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR

from click import Argument, Command, FloatRange, IntRange, Option, Path
from click.exceptions import ClickException

from nichtparasoup._internals import _log, _logging_init
from nichtparasoup.config import Config
from nichtparasoup.testing.config import PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT, ConfigFileTest, ConfigTest


def main(file: str, *,
         probe: bool = True, probe_retries: int = PROBE_RETRIES_DEFAULT, probe_delay: float = PROBE_DELAY_DEFAULT,
         debug: bool = False) -> None:  # pragma: no cover
    _logging_init(L_DEBUG if debug else L_ERROR)
    _log('debug', 'ConfigFile: {}'.format(file))
    config = _validate_file(file)
    if probe:
        _probe_config(config, retries=probe_retries, delay=probe_delay)


def _validate_file(file: str) -> Config:  # pragma: no cover
    try:
        return ConfigFileTest().validate(file)
    except Exception as e:
        raise ClickException('ValidateError: {!s}'.format(e)) from e


def _probe_config(config: Config, *, retries: int, delay: float) -> None:  # pragma: no cover
    config_test = ConfigTest()
    try:
        config_test.probe(config, delay=delay, retries=retries)
    except Exception as e:
        raise ClickException('ProbeError: {!s}'.format(e)) from e


cli = Command(
    name='server-config-check',
    help='Validate (and probe) a YAML config file.',
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
            param_decls=['--debug'],
            help='Enable debug output.',
            is_flag=True,
        ),
    ]
)

if __name__ == '__main__':
    cli.main()
