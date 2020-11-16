# test

stick to these rules:

* add your tests somewhere in dir `function`/`integration`/`unit`.
* write the test for `pytest` with `pytest-mock` in mind. `assert`-style preferred over python's `unittest`.
* each testable package/module has its own folder: name the test folder `test_*`.
* each testable function/class has its own file:   name the test file   `test_*.py`.
* name the test functions `test_*`.
* put test data in a folder called `testdata_*`.

## write tests

install test requirements:
```shell script
# run from project root:
python3 -m pip install \
  -e . \
  -r requirements/tests.txt \
  -c requirements/dev.txt
```

then write your tests.  

## run tests

### plain

```shell script
# run from project root:
python3 -m pip install \
  -e . \
  -r requirements/tests.txt \
  -c requirements/dev.txt
python3 -m pytest
```

### via tox 

```shell script
# run from project root:
python3 -m pip install -r requirements/tox.txt -c requirements/dev.txt
python3 -m tox -e py
```
