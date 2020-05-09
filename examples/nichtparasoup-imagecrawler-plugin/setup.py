"""Setup for old tools that don't implement PEP517 & PEP518
Modern setup is triggered via `pyproject.toml`.

This script is still needed for the following purposes:
* `pip install --editable` which calls this file directly, until `pip`-developers finds a solution.
  ATTENTION: `pip install`'s `--editable` flag might requires the `--no-build-isolation` flag.
* dependency analyzers that don't support `setup.cfg`, yet.
"""
import setuptools

if __name__ == '__main__':
    setuptools.setup(
        # actual config is done via `setup.cfg`
    )
