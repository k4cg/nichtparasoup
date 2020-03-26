# install

1. download/clone this repo
1. change into the directory of this implementation
1. install via `python3 -m pip install .`  
   *ATTENTION*: `pip3 install -e` might be broken for `pyproject.toml` based builds.
   This is a known [issue](https://github.com/pypa/pip/issues/6375).
   A workaround is to install ala `python3 -c 'import setuptools; setuptools.setup();' develop --user`.
