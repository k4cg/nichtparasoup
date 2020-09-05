# Release process

## General

1. if needed: bring the changes into the `master` branch.
1. File changes:
   * bump the `__version__` in `src/nichtparasoup/__init__.py`
   * set the version & release-date in `HISTORY.md` to mark "unreleased" changes as released ones
1. tag the version on `master` branch
   * use the exact value of `__version__` in `src/nichtparasoup/__init__.py`.  
   * the release workflow will check version match of tag, package and source
1. create a release in GitHub
   * point to the version's tag on `master` branch
   * copy/past the current release notes from `HISTORY.md`

That's it,  
the publishing is automated via [github workflow](../.github/workflows/python-package-release.yaml).

## Major version split

This happens when the development of a next major version starts:
simply branch away from master into a `{MAJOR}.0-dev` branch.
When the version is ready, merge the dev branch back to master.
