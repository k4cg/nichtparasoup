# test

## write tests

```shell script
python3 -m pip install -e .[testing]
```

then write your tests.  
add additional needed requirements to the "testing" extras in `../setup.py`.


## run tests

```shell script
python3 -m pip install -e .[testing]
python3 -m coverage run -m pytest 
```

then, to gather test coverage:

```shell script
python3 -m coverage report -m 
python3 -m coverage html 
```


### via tox 

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
  -it --rm \
  python:3.4 bash -c \
  "pip install tox; python -m tox"
```

## reports 

* after running, a report will be shown
* for coverage report see `python -m coverage`

## contribution 

stick to these rules:

* add your tests somewhere in this dir
* write the test - use `unittest` or simply `assert`
* name the test file `*_test.py`
* name the test functions `test_*`
* name call the test classes `*Test`
