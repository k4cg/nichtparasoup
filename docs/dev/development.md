# Development

_TODO_

This documentation is work in progress.   
Reach out to [jkowalleck](https://github.com/jkowalleck) to ask for help.


## Backend

Install the requirements: `ptyhon3 -m pip install -e .[development]`.  
*ATTENTION*: `pip`'s option `--editable` in combination with `--user` might be broken for `pyproject.toml` based build envs.
This is a known [issue](https://github.com/pypa/pip/issues/6375).  
A workaround would be to call `python3 setup.py develop --user -e -b build` manually.

Then just do whatever you would like.  

After writing the code have the code fixed via
[`isort`](https://pypi.org/project/isort/) and
[`autopep3`](https://pypi.org/project/autopep3/).   
These tools are already installed via `development` dependencies.

Do not forget to [test](testing.md) the code.  
This will also check for
import order (fix via `isort`) and
pycodestyle (fix via `autopep8`).

## Image crawler

_TODO_


## Frontend

_TODO_
