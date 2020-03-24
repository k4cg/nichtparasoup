# Development

_TODO_

This documentation is work in progress.   
Reach out to [jkowalleck](https://github.com/jkowalleck) to ask for help.


## Backend

Install the requirements: `python -m pip install .[development]`.  
*ATTENTION*: `pip install -e` might be broken for `pyproject.toml` based builds.
This is a known [issue](https://github.com/pypa/pip/issues/6375).

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
