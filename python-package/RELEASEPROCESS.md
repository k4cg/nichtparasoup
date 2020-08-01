# Release process


## General

1. if needed: bring the changes into the `master` branch.
1. File changes:
   * bump the `__version__` in `src/nichtparasoup/__init__.py`
   * set the version in `HISTORY.md` to mark "unreleased" changes are released ones
1. tag the version om MASTER/MAJOR branch 
   with the value of `__version__` in `src/nichtparasoup/__init__.py`
1. create a release in GitHub
   * point tho the version's tag om MASTER/MAJOR branch
   * copy/past the release notes from `HISTORY.md` 

That's it, hte rest is automated via gh-workflow.

## Major version split

This happens when the development of a next major version starts:  
simply branch away from master into a `{MAJOR}.0-dev` branch.
when the version is ready, merge the dev branch back to master.
