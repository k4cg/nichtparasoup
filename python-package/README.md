# nichtparasoup

[![shield_pypi-python]][link_pypi]
[![shield_pypi-version]][link_pypi]  
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_sonar-quality]][link-sonar-dashboard]
[![shield_sonar-coverage]][link_sonar-coverage]

----

_nichtparasoup_ is a hackspaces entertainment system.
It randomly displays images from
[instagram](https://instagram.com),
[pr0gramm](https://pr0gramm.com) and
[reddit](https://reddit.com).  
Other crawlers are currently removed, but will be back soon.

If you find an ImageCrawler for your favourite ImageBoard missing, feel free to write an own ImageCrawler therefore.  
Contribute it to the _nichtparasoup_ project or write it as an independent plugin :-)


![logo](https://raw.githubusercontent.com/k4cg/nichtparasoup/3.0-dev/python-package/images/logo.png)


---


At our hackspace [k4cg](https://k4cg.org) we use it since years now.  
It turns out to be a very non-invasive way of entertaining a crowd of nerds 
without having the noise and interruptions of videos or other stuff.

Here is what it looks like in your browser
![screenshot](https://raw.githubusercontent.com/k4cg/nichtparasoup/3.0-dev/python-package/images/screenshot.png)

and even better, on a video projector in your local hackspace!
![hackspace](https://raw.githubusercontent.com/k4cg/nichtparasoup/3.0-dev/python-package/images/hackspace.jpg)


## How it works

Images are crawled from multiple public pre-configured sources.  
No image is actually downloaded, just the URL to images are gathered. Found images are kept in a list, also it is
assured that the same URL is never gathered twice.

To display the crawled images, _nichtparasoup_ starts a web-server display a web UI.  
The web UI fetches a random image URL from the _nichtparasoup_ server one by one. 

The web UI will load new images continuously, unless one of the following events happen:
* paused manually in the web UI
* scroll position in web UI is not on top
* window or tab lost focus
* web UI is in image theater/zoom mode
* boss mode is active in web UI

In the web UI the images are downloaded from the original source. Also the original source is linked and marked by
an icon. Just hover or click the icon in the bottom right of an image.

Every time _nichtparasoup_ serves an image URL it also removes it from its list. This means an image URL is served
only once - unless the server was reset. (This might change in the future)


## Demo

Visit [nicht.parasoup.de/demo/](http://nicht.parasoup.de/demo/) to try it!


## Install, Usage, Config, etc

see the [docs](https://github.com/k4cg/nichtparasoup/tree/3.0-dev/python-package/docs/index.md).

## License

MIT - see the [`LICENSE`](https://github.com/k4cg/nichtparasoup/blob/3.0-dev/python-package/LICENSE) file for details.


## Credits

* code is written by the authors shown 
  at the [source code repository](https://github.com/k4cg/nichtparasoup/3.0-dev/python-package).
* parts of the logo are taken
  from [Smashicons](https://www.flaticon.com/authors/smashicons)
  on [www.flaticon.com](https://www.flaticon.com/)
  are licensed [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/).



[shield_pypi-version]: https://img.shields.io/pypi/v/nichtparasoup?logo=PyPI&logoColor=white "PyPi release-version"
[shield_pypi-python]: https://img.shields.io/pypi/pyversions/nichtparasoup?logo=Python&logoColor=white "PyPi py-versions"
[shield_gh-workflow-test]: https://img.shields.io/github/workflow/status/k4cg/nichtparasoup/Test%20PythonPackage/3.0-dev?logo=GitHub%20Actions&logoColor=white "test status"
[shield_sonar-quality]: https://img.shields.io/sonar/quality_gate/nichtparasoup:PythonPackage?server=https%3A%2F%2Fsonarcloud.io&logo=SonarCloud&logoColor=white "quality"
[shield_sonar-coverage]: https://img.shields.io/sonar/coverage/nichtparasoup:PythonPackage?server=https%3A%2F%2Fsonarcloud.io&logo=SonarCloud&logoColor=white "coverage"
[shield_codecov]: https://img.shields.io/codecov/c/github/k4cg/nichtparasoup/3.0-dev?logo=Codecov&logoColor=white "civerage"
[link_pypi]: https://pypi.org/project/nichtparasoup/
[link_gh-workflow-test]: https://github.com/k4cg/nichtparasoup/actions?query=workflow%3A%22Test+PythonPackage%22+branch%3A3.0-dev
[link-sonar-dashboard]: https://sonarcloud.io/dashboard?id=nichtparasoup%3APythonPackage
[link_sonar-coverage]: https://sonarcloud.io/component_measures?id=nichtparasoup%3APythonPackage&metric=coverage
[link_codecov]: https://codecov.io/gh/k4cg/nichtparasoup/tree/3.0-dev/python-plugin-example
