# Release process


## General

1. if needed: bring the changes into the MAJOR version's branch.
1. File changes:
   * bump the `__version__` in `src/nichtparasoup/__init__.py`
   * set the version in `HISTORY.md` to mark "unreleased" changes are released ones
1. tag the version om MASTER/MAJOR branch 
   with the value of `__version__` in `src/nichtparasoup/__init__.py`
1. create a release in GitHub
   * point tho the version's tag om MASTER/MAJOR branch
   * copy/past the release notes from `HISTORY.md` 

thats it, hte rest is automated via gh-workflow.

## Major version split

This happens when the development of a next major version starts.

The current master gets branched out to allow patching the current version.  
The master keeps on moving forward as usual.

Steps:
1. create a new branch `{MAJOR}.x` from master
1. for that MAJOR version's branch:
   * in github > Settings > Branches  
    set the branch protection rules
    to be the same as on current master.
   * adapt the `README.md`: make URLs to target the branch
   * set the `__version__` in `src/nichtparasoup/__init__.py`
    to current `{MAJOR}.{MINOR}.{PATCH}`
   * set the version in `HISTORY.md` to mark "unreleased" changes are released ones




1. 
