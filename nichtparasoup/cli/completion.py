__all__ = ['main', 'cli']

from typing import Any, Optional

from click import Choice, Command, Option, echo
from click_completion import Shell, get_code, init  # type: ignore

# click's builtin completion is insufficient and partially broken.
# completes loaded sub commands as 'main' instead of the correct name
init()


# @FIXME unfortunately there is no proper completion for files
# @FIXME and since there is no support for manual `autocomplete` callbacks, i cannot patch it in ...
#   - see https://github.com/click-contrib/click-completion/pull/27


def main(shell: Optional[Shell]) -> None:  # pragma: no cover
    echo(get_code(shell=shell, prog_name='nichtparasoup'))


_shell_choices_text = sorted(s.name for s in Shell)


def _cls_make_shell(_: Any, __: Any, shell: Optional[str]) -> Optional[Shell]:  # pragma: no cover
    return Shell[shell] if shell else None


cli = Command(
    name='completion',
    help='Emit completion code for the shell.',
    callback=main,
    params=[
        Option(
            param_decls=['--shell'],
            help='Override auto-detection. [{}]'.format('|'.join(_shell_choices_text)),
            metavar='SHELL',
            type=Choice(_shell_choices_text),
            default=None,
            callback=_cls_make_shell,
        )
    ]
)

if __name__ == '__main__':
    cli.main()
