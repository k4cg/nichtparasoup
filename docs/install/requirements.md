# requirements

see [install docs](index.md) first.

This package requires `Python>=3.6`!

Required dependencies are installed automatically during install via `pip`.

If you find the installation breaking, this might be due to the following issues:

## packages can not be installed globally

solution: add the `--user` switch to your `pip install` command.

## dependencies version conflict

_nichtparasoup_ is using some dependencies in a certain minimal version.

if you have issues with already installed package versions,
just use
[python's `venv`](https://docs.python.org/3/library/venv.html) or
[`pipx`](https://pypi.org/project/pipx/).
