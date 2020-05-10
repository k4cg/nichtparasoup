# Changelog

## Unreleased

! upcoming version will be `3.0.0` of __nichtparasoup__ !
see the [milestone tracking at github](https://github.com/k4cg/nichtparasoup/milestone/2).

* Breaking changes
  * CommandLine Interface overhaul. See cli help via `nichtparasoup --help`.
    * CLI is done via `click` now.
    * Shell completion was removed temporary. See the [issue](https://github.com/k4cg/nichtparasoup/issues/226).
    * Proper subcommands are used now.
  * API
    * `Crawler.type` of to `status/crawlers` API is now a fill qualified class name.
      See the [docs](docs/web_api/status_crawlers.md).  
      The old short-typed version is still available as the optional `Crawler.name` 
      (optional means: can be missing or `null`, if manually added).
  * Package `nichtparasoup.imagecrawler` was renamed to `nichtparasoup.imagecrawlers`.
    Everything needed to implement an imagecrawler was moved to a clean module `nichtparasoup.imagecrawler`.
  * Class `nichtparasoup.testing.config.ConfigFileTest` was moved to `nichtparasoup.testing.configfile.ConfigFileTest`.

* Changes
  * Class `nichtparasoup.core.server.ServerStatus` is not abstract anymore.
  * `nichtparasoup.VERSION` was moved to `nichtparasoup.__version__`, therefore
      `nichtparasoup.__version__` is no longer a module but a string.
  * Package `nichtparasoup.testing` hot a huge overhaul. 
    * Classes do no longer implement `unittets.Testcase` anymore.
    * Functionality was split into chunks for easier use.
    * Class  `nichtparasoup.testing.configfile.ConfigFileTest` 
      (previously `nichtparasoup.testing.config.ConfigFileTest`) 
      was reworked.

* Added
  * API: `Crawler.name` to `status/crawlers` API. See the [docs](docs/web_api/status_crawlers.md).
  * Public CLI modules `nichtparasoup.commands.*` for use via `python3 -m`:
    * `nichtparasoup.commands.imagecrawler_desc`
    * `nichtparasoup.commands.imagecrawler_list`
    * `nichtparasoup.commands.server_config_check`
    * `nichtparasoup.commands.server_config_dump_defaults`
    * `nichtparasoup.commands.server_run`
  * Public CLI module `nichtparasoup.cli.main` for use via `python3 -m`.
  * Class `nichtparasoup.testing.config.ConfigTest` was added.
  * Property `nichtparasoup.core.server.Server.stats` was made available to the public.
  * Implementations of `nichtparasoup.core.imagecrawer.BaseImageCrawler`
    * Function `get_internal_name()` to return the internal name.
      If instance was made via `nichtparasoup.config.get_imagecrawler()` the value is set
      to represent the "name" from the config.
    * Property `internal_name` - read-only shortcut for `get_internal_name()`.
    * Function `__str__()` .  
      Returns `<NamedImagecrawler {INTERNAL_NAME} {CONFIG}>` if `internal_name` is set, 
      otherwise the behaviour falls back to `__repr__()`.

Removed:
  * `nichtparasoup.core.server.type_module_name_str()`

* Misc
  * Build process is now isolated and conform to
    [PEP517](https://www.python.org/dev/peps/pep-0517/) &
    [PEP518](https://www.python.org/dev/peps/pep-0518/).  
    *ATTENTION*: `pip install`'s `--editable` flag might requires the `--no-build-isolation` flag.
  * Improved some [docs](docs).
  * internal
    * All internal imports were made relative (again).
    * Logging reviewed, uses %-strings as params, now.
    * `try`/`except` got some overhaul to cover needed parts, only.
    * CLI is now powered by [`click`](https://click.palletsprojects.com).
      Was made via `argparse` before.
  * Removed `ddt` from the testing dependencies. Closes [issue #233](https://github.com/k4cg/nichtparasoup/issues/233).
  * version-bumped some dependencies
  


## 2.4.1

* Fixed
  * commandline completion for config files to properly suggest `*.yaml` & `*.yml` files.

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
