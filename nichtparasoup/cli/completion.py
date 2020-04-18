__all__ = ["main"]

from typing import Optional

from click import Choice, command, echo, option
from click_completion import Shell, get_code, init  # type: ignore

# click's builtin completion is insufficient and partially broken.
# completes loaded sub commands as 'main' instead of the correct name
init()

ShellChoice = Choice(Shell.__members__.keys())


@command(name='completion')
@option('--shell', type=ShellChoice, default=None, metavar='SHELL',
        help='Override auto-detection. Values: {}.'.format(', '.join(ShellChoice.choices)))
def main(shell: Optional[Shell]) -> None:  # pragma: no cover
    """Emit completion code for the shell.

    Enables the shell to auto-complete nichtparasoup commands and options.
    """
    echo(get_code(shell=shell, prog_name='nichtparasoup'))
