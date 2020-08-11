# test

stick to these rules:

* add your tests somewhere in this dir
* write the test for `pytest`. `assert`-style preferred over python's `unittest`.
* each testable package/module has its own folder: name the test folder `test_*`
* each testable function/class has its own file:   name the test file   `test_*.py`
* test files are performed in alphabetical order - so add a number to have them ordered
* name the test functions `test_*`
* put test data in a folder called `testdata_+`


## write tests

install test requirements.

then write your tests.  
add additional needed requirements to the respective [requirements file](../../requirements/tests.txt).


### run tests via tox 

```shell script
# run from project root:
python -m pip install -r requirements/tox.txt
python -m tox
```

```shell script
# run from project root:
docker run \
  --name nichtparasoup-testing \
  -v "$PWD":/usr/src/nichtparasoup \
  -w /usr/src/nichtparasoup \
  --rm \
  python:3.8 bash -c \
  "python -m pip install wheel setuptools pip && python -m pip install -r requirements/tox.txt && python -m tox; rm -rf .tox;"
```
