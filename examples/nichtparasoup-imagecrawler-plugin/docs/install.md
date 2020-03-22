# install

1. download/clone this repo
1. change into the directory of this implementation
1. install via `python3 -m pip install .`  
   *ATTENTION*: `pip`'s option `--editable` in combination with `--user` might be broken for `pyproject.toml` based build envs.
   This is a known [issue](https://github.com/pypa/pip/issues/6375).  
   A workaround would be to call `python3 setup.py develop --user -e -b build` manually.
