# Changelog

## Unreleased

add upcoming unreleased modifications here

## 2.5.0

* Breaking changes
  * commandline interface changed. See cli help via `nichtparasoup --help`.

## 2.4.1

* Fixed
  * commandline autocompletion for config files to properly suggest `*.yaml` & `*.yml` files.

## 2.4.0

* Changes
  * upgraded dependency `werkzeug` from `>=0.15` to `>=1.0`.
  * dependencies pinned to greater/equal current(latest) minor version.
* Fixed
  * issue [#187](https://github.com/k4cg/nichtparasoup/issues/187).
* Added
  * commandline autocompletion via [`argcomplete`](https://pypi.org/project/argcomplete/).

## 2.3.1

* Fixed
  * paging of the `Pr0gramm` ImageCrawler in `promoted=True` mode.

## 2.3.0

* Breaking changes
  * `nichtparasoup config --check`'s "duplicate image crawler" is no longer a Warning but an Error.
  * renamed `nichtparasoup.testing.config.ConfigFilesTest` to `ConfigFileTest` - without an "s".
* Changed
  * `nichtparasoup config --check` now does a probe crawl.
  * class `ImageCrawlerInfo` lost support for positional arguments, supports keyword-arguments only - prepare future extensibility.
  * class `Image` lost support for positional arguments, supports keyword-arguments only - prepare future extensibility.
* Added
  * image crawler for [pr0gramm](https://pr0gramm.com) - Read the [docs](./docs/imagecrawlers/pr0gramm.md).
  * additional test function: `nichtparasoup.testing.config.ConfigFileTest.probe()`.

## 2.2.2

* Fixed
  * exception catch in `instagram` imagecrawler.
  * hyperlinks in the `README.md`.
* Added
  * keywords in `setup.py`.

## 2.2.1

* Fixed
  * web UI settings storage.

## 2.2.0

* Breaking changes
  * in the config the crawlers' `type` was renamed to `name`.
  * the `Dummy` ImageCrawler was renamed to `Echo`.
* Changed
  * `ImageCrawlerInfo`'s `desc` was renamed to `description`.
  * `ImageCrawlerInfo` don't require a `version` anymore.
* Fixed
  * the non-existing `favicon.ico` is no longer tried to be loaded.
* Added
  * plugin support for ImageCrawlers. You may write your own, now :-)
    * plugin recognition via EntryPoint "nichtparasoup_imagecrawler".
    * [`testing`](nichtparasoup/testing) added: test helpers are now part of the package for public use by plugin-devs.
    * [`example`](examples/nichtparasoup-imagecrawler-plugin) implementation added.
    * [`doc`](docs/plugin-development) space was prepared.
  * commandline interface got a `--debug` switch to help plugin developers.
  * `webserver` now uses [`mako`](https://www.makotemplates.org/) template engine.
  * `ImageCrawlerInfo` may have an `icon_uri`, now.
  * `ImageCrawlerInfo` may have a `long_description`, now.

## 2.1.1

* Fixed
  * auto-play is no longer broken, when image-gallery-mode is canceled by browser's builtin functions.

## 2.1.0

* Added
  * ImageCrawler for Instagram: `InstagramProfile` & `InstagramHashtag`.
  * web UI: added image zoom.
  * web UI: hide scroll bar in FullScreen mode, when at scroll position is at top.

## 2.0.1

* Fixed
  * internal version detection.

## 2.0.0

Rewrite from scratch.

* Breaking changes
  * removed support for python2.7 and lower.
  * removed support for python3.4 and lower.
  * the config format completely changed. Read the `docs/` for more.
  * everything changed ... due to a complete rewrite. Read the `docs/dev/` for more.
* Added
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
* Modified
  * `README.md` to match current implementation
  * web UI to match latest web serve specs* rewrote from scratch
  * config system - now using `YAML` file format
  * core image crawler architecture
  * core server
  * web server
  * command line interface
  * reddit crawler
* Removed
  * Some image crawlers were removed, so they can be rewritten from scratch.
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
