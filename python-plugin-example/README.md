# _nichtparasoup_ ImageCrawler: Placeholders

[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_sonar-quality]][link-sonar-dashboard]
[![shield_sonar-coverage]][link_sonar-coverage]

----

This is an example plugin for [_nichtparasoup_](https://pypi.org/project/nichtparasoup/).  
Purpose of this project is, to give ImageCrawler plugin developers a kick start.

This project includes:
* simple demo implementation [`nichtparasoup_placeholders`](src)
* _nichtparasoup_ [example config](examples)
* some **minimal** [`docs`](docs)
* rules fo static code analysis and type-checks via `mypy`
* preparation for unit tests via `pytest`
* **minimal** setup config [`setup.cfg`](setup.cfg)
* some **minimal** project setup configs

For details how write a ImageCrawler plugins,
see the [dedicated docs](../python-package/docs/dev/plugin-development/index.md). 



[shield_gh-workflow-test]: https://img.shields.io/github/workflow/status/k4cg/nichtparasoup/Test%20PythonPluginExample/3.0-dev "test status"
[shield_sonar-quality]: https://img.shields.io/sonar/quality_gate/nichtparasoup:PythonPluginExample?server=https%3A%2F%2Fsonarcloud.io "quality"
[shield_sonar-coverage]: https://img.shields.io/sonar/coverage/nichtparasoup:PythonPluginExample?server=https%3A%2F%2Fsonarcloud.io "coverage"
[shield_codecov]: https://img.shields.io/codecov/c/github/k4cg/nichtparasoup/3.0-dev "civerage"
[link_gh-workflow-test]: https://github.com/k4cg/nichtparasoup/actions?query=workflow%3A%22Test+PythonPluginExample%22+branch%3A3.0-dev
[link-sonar-dashboard]: https://sonarcloud.io/dashboard?id=nichtparasoup%3APythonPluginExample
[link_sonar-coverage]: https://sonarcloud.io/component_measures?id=nichtparasoup%3APythonPluginExample&metric=coverage
[link_codecov]: https://codecov.io/gh/k4cg/nichtparasoup/tree/3.0-dev/python-package
