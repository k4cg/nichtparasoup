# Changelog

## 3.0.0

Unreleased
-- see the [milestone tracking at github](https://github.com/k4cg/nichtparasoup/milestone/2).

## 3.0.0a1

* Breaking changes
  * Requires `python>=3.6` -- was `python>=3.5`.
  * [CommandLine Interface](docs/run/index.md) overhaul. See cli help via `nichtparasoup --help`.
    * CLI is done via [`click`](https://click.palletsprojects.com) now (was done via `argparse` before).
    * Shell completion was removed temporary. See the [issue](https://github.com/k4cg/nichtparasoup/issues/226).
    * Proper subcommands are used now.  
      Also available via `python3 -m nichtparasoup.commands.*` - see in added feature section below.
  * Web-API: 
    * `version` of `/status/server` was moved to `/status`.
    * `Crawler.type` of `/status/crawlers` is now a full qualified class name.
      See the [docs](docs/web_api/status/crawlers.md).  
      The old short-typed version is still available as the optional `Crawler.name` 
      (optional means: can be missing or `null`, if manually added).
  * Package `nichtparasoup.imagecrawler` was renamed to `nichtparasoup.imagecrawlers`.
    Everything needed to implement an imagecrawler was moved to a clean module `nichtparasoup.imagecrawler`.
  * Class `nichtparasoup.testing.config.ConfigFileTest` was moved to `nichtparasoup.testing.configfile.ConfigFileTest`.
    Also it behaves different now. Read the code and annotations for a deeper insight.
  * Some Class methods of `nichtparasoup.core.server.Server` got reworked return types:
    * `Server.get_image()` returns optional `nichtparasoup.core.server.ImageResponse` -- was optional `dict`.
    * `Server.refill()` returns `None` -- was `dict`.
    * `Server.request_reset()` returns `nichtparasoup.core.server.ResetResponse` -- was `dict`.
  * Changes to `nichtparasoup.core.ServerRefiller.__init__()`: 
    * Parameter `sleep` was renamed to `delay` and is nof `loat` (was `int` or `float`). 
  * Class `nichtparasoup.core.server.Status` was removed.  
    Its former static methods that returned dictionaries were reworked to be DataClasses:
    * `nichtparasoup.core.server.ServerStatus`    -- replaces `.Status.server()`.
    * `nichtparasoup.core.server.CrawlerStatus`   -- replaces `.Status.crawlers()`.
    * `nichtparasoup.core.server.BlacklistStatus` -- replaces `.Status.blacklist()`.
  * Removed the install-extras `development` and `testing`.
  * Defaulting arguments of `nichtparasoup.core.Crawler.__init__()` became kwargs.
  * Arguments of `nichtparasoup.core.Crawler.fill_up_to()` changed:
    * `filled_by` became a kwarg.
    * `timeout` became a kwarg and was renamed to `delay`.
  * Arguments of `nichtparasoup.core.NPCore.fill_up_to()` changed:
    * `on_refill` became a kwarg.
    * `timeout` became a kwarg and was renamed to `delay`.
  * Some arguments of `nichtparasoup.core.NPCore.add_imagecrawler()` became kwargs and got default values.
  * Arguments of `nichtparasoup.core.imagecrawler.RemoteFetcher` became kwargs.
  * Method `nichtparasoup.core.imagecrawler.BaseImageCrawler.__init__()` became abstract 
    in favour of proper argument definition and typing in implementations
  * All builtin imagecrawlers' `__init__()` got proper argument definition and typing
    as they are implementations of `nichtparasoup.core.imagecrawler.BaseImageCrawler.__init__()`.
  * Package `nichtparasoup.testing` got a huge overhaul. 
    * Classes do no longer implement `unittets.TestCase` anymore.
    * Functionality was split into chunks for easier use.
    * Class `.configfile.ConfigFileTest` (previously named `.config.ConfigFileTest`) was reworked.
    * Class `.imagecrawler.FileFetcher` supports fully qualified urls now, including schema and netloc.
      Therefore an optional argument `base_url` was added.
  * Server's imagecrawler can get exhausted when the crawling source's end is reached.
    Resolves [issue #152](https://github.com/k4cg/nichtparasoup/issues/152).
* Removed:
  * `nichtparasoup.core.server.type_module_name_str()`
  * `development` and `testing` extras were removed. replaced by files in `requirements/` folder. See "changes".
* Changes
  * Method `nichtparasoup.code.Crawler.crawl()` returns number of actually added images, was number of crawled images.
  * `nichtparasoup.core.imagecrawler.ImageRecognizer` also detects `.webp`.
  * `nichtparasoup.core.imagecrawler.BaseImageCrawler` does not call `self._reset()` on first run anymore.
  * Class `nichtparasoup.core.server.ServerStatus` is not abstract anymore.
  * `nichtparasoup.VERSION` was moved to `nichtparasoup.__version__`, therefore
    `nichtparasoup.__version__` is no longer a module but a string.
  * Install-extras `development` and `testing` were changed to be separate (`pip-compile`d pinned) files:
    * [dev requirements](requirements/dev.txt)
    * [tests requirements](requirements/tests.txt)
* Fixed
  * False-positives in `nichtparasoup.core.imagecrawler.ImageRecognizer.path_is_image()`.
  * Fixed a possible endless loop of `nichtparasoup.code.Crawler.fill_up_to()`.
* Added
  * Web-API: `Crawler.name` to `status/crawlers` API. See the [docs](docs/web_api/status/crawlers.md).
  * Public CLI package `nichtparasoup.cli` for use via `python3 -m`.
  * Public CLI command modules for use via `python3 -m`:
    * `nichtparasoup.commands.imagecrawler_desc`
    * `nichtparasoup.commands.imagecrawler_list`
    * `nichtparasoup.commands.server_config_check`
    * `nichtparasoup.commands.server_config_dump_defaults`
    * `nichtparasoup.commands.server_run`
  * Class `nichtparasoup.webserver.WebServer` got an optional argument `developer_mode` (default: `False`)
    which enables an insecure web-developer mode and sets
    [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) to "*".
  * Class `nichtparasoup.testing.config.ConfigTest` was added.
  * Property `nichtparasoup.core.server.Server.stats` was made available to the public.
  * New classes in `nichtparasoup.core.server` were added to 
    represent response types of `nichtparasoup.core.server.Server`'s methods:
    * `.ResetResponse` represents response of `.Server.request_reset()`.
    * `.ImageResponse` represents response of `.Server.get_image()`.
  * New DataClasses were added to module `nichtparasoup.core.server`:
    * `.ServerStatus`
    * `.CrawlerStatus`
    * `.BlacklistStatus`
  * `nichtparasoup.core.Crawler` got a new kwarg `restart_at_front_when_exhausted`.  
    `nichtparasoup.core.NPCore.add_imagecrawler()` got a new kwarg `restart_at_front_when_exhausted`.  
    See the [docs](docs/config/index.md)
  * Implementations of `nichtparasoup.core.imagecrawer.BaseImageCrawler` got new features:
    * Method `.get_internal_name()` to return the internal name.
      If instance was made via `nichtparasoup.config.get_imagecrawler()` the value is set
      to represent the "name" from the config.
    * Property `.internal_name` - read-only shortcut for method `.get_internal_name()`.
    * Method `.__str__()` .  
      Returns `<NamedImagecrawler {INTERNAL_NAME} {CONFIG!r}>` if `internal_name` is set, 
      otherwise the behaviour falls back to `__repr__()`.
  * Public stuff in module `nichtparasoup.imagecrawers.instagram` (was nonpublic before):
    * Class `.BaseInstagramCrawler` became public. (since it does `Lock()` allocation automatically, now.)
    * Class `.InstagramQueryHashFinder` became public for extending `.BaseInstagramCrawler`.
    * Constants `.INSTAGRAM_URL_ROOT` and `.INSTAGRAM_ICON_URL` became public for extending `.BaseInstagramCrawler`.
* Misc
  * Build process is now isolated and conform to
    [PEP517](https://www.python.org/dev/peps/pep-0517/) &
    [PEP518](https://www.python.org/dev/peps/pep-0518/).  
    *ATTENTION*: `pip install`'s `--editable` flag might requires the `--no-build-isolation` flag.
  * Improved some [docs](docs/index.md). Added an `index.md` to all folders. restructured some docs.
  * Internal
    * All internal imports were made relative.
    * Logging reviewed, uses `%`-strings as params, now.
    * `try`/`except` got some overhaul to cover needed parts, only.
  * Removed `ddt` from the testing dependencies. Closes [issue #233](https://github.com/k4cg/nichtparasoup/issues/233).
  * Version-bumped some dependencies, pinned dev dependencies via `pip-compile`.
  * Added some more tests.
  * improved `venv` support when it comes to testing.
  * Tests via `tox` were split.
    Code style tests are done via own test named `style` now (was part of standard tests).
  * Repo layout changed to be a monorepo. See [the repo](https://github.com/k4cg/nichtparasoup).  
    This also means, that the plugin-example was moved out of the project into an own project.

## 2.4.2

Released 2020-06-20

* Fixed
  * config yaml parser when `yamale>=2.1` is installed.

## 2.4.1

Released 2020-02-21

* Fixed
  * commandline completion for config files to properly suggest `*.yaml` & `*.yml` files.

## 2.4.0

Released 2020-02-21

* Changes
  * upgraded dependency `werkzeug` from `>=0.15` to `>=1.0`.
  * dependencies pinned to greater/equal current(latest) minor version.
* Fixed
  * issue [#187](https://github.com/k4cg/nichtparasoup/issues/187).
* Added
  * commandline autocompletion via [`argcomplete`](https://pypi.org/project/argcomplete/).

## 2.3.1

Released 2020-01-28

* Fixed
  * paging of the `Pr0gramm` ImageCrawler in `promoted=True` mode.

## 2.3.0

Released 2020-01-26

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

Released 2020-01-12

* Fixed
  * exception catch in `instagram` imagecrawler.
  * hyperlinks in the `README.md`.
* Added
  * keywords in `setup.py`.

## 2.2.1

Released 2019-12-20

* Fixed
  * web UI settings storage.

## 2.2.0

Released 2019-12-20

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

Released 2019-11-28

* Fixed
  * auto-play is no longer broken, when image-gallery-mode is canceled by browser's builtin functions.

## 2.1.0

Released 2019-11-28

* Added
  * ImageCrawler for Instagram: `InstagramProfile` & `InstagramHashtag`.
  * web UI: added image zoom.
  * web UI: hide scroll bar in FullScreen mode, when at scroll position is at top.

## 2.0.1

Released 2019-11-26

* Fixed
  * internal version detection.

## 2.0.0

Released 2019-11-26

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

Rolling releases in repository
until 2019-10-10

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
