# test

## write tests

install test requirements.

then write your tests.  
add additional needed requirements to the "testing" extras in `../setup.cfg`.


### run tests via tox 

```shell script
# run from project root:
python3 -m pip install --upgrade tox
python3 -m tox
```

```shell script
# run from project root:
docker run \
  --name nichtparasoup-testing \
  -v "$PWD":/usr/src/nichtparasoup \
  -w /usr/src/nichtparasoup \
  --rm \
  python:3.6 bash -c \
  "python3 -m pip install tox; python3 -m tox; rm -rf .tox;"
```

## contribution 

stick to these rules:

* add your tests somewhere in this dir
* write the test with`unittest`: test cases inherit `unittest.TestCase.`
* each testable package/module has its own folder: name the test folder `test_*`
* each testable function/class has its own file:   name the test file   `test_*.py`
* test files are performed in alphabetical order - so add a number to have them ordered
* name the test functions `test_*`
