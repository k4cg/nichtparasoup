# Changelog


## Unreleased


## 2.0.1

### Fix

* internal version detection


## 2.0.0

Rewrite from scratch.

### Breaking changes

* removed support for python2.7 and lower.
* removed support for python3.4 and lower.

#### For users

the config format completely changed. Read the `docs/` for more.

#### For developers

Yes, everything changed ... due to a complete rewrite. Read the `docs/dev/` for more.

### Added

* publishing to PyPI
* image crawler for "picsum"
* image crawler "dummy"
* documentation in `docs/`
* `setup.py`-based packaging support - for `PIP`
* testing support via `pytest` and test coverage report via `coverage`
* code style tests via `flake8`, `mypy` and extensions for those - also added them to `tox`-based automatisation
* `tox`-based automatisation for testing
* CI tests for `tox`-based tests on `py35`, `py36`, `py37`, `py38` - via github actions
* version history file `HISTORY.md`

### Modified

* `README.md` to match current implementation
* web UI to match latest web serve specs### rewrote from scratch

* config system - now using `YAML` file format
* core image crawler architecture
* core server
* web server
* command line interface
* reddit crawler

### Removed

Some image crawlers were removed, so they can be rewritten from scratch.

* image crawler for "giphy"
* image crawler for "soup.io"
* image crawler for "pr0gramm"
* image crawler for "4chan"
* image crawler for "9gag"


## 1.x.x

basic feature complete implementation

* supports: python2.6 and later
* supports: python3.4 and later
* implemented: config system - using `INI` file format
* implemented: commandline interface
* implemented: web UI
* implemented: web server
* implemented: core server architecture to draw a random crawled image
* implemented: image crawler for giphy, soup.io, pr0gramm, 4chan, 9gag, reddit
* implemented: image crawler architecture
