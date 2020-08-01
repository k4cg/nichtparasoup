# Development

**TODO**

This documentation is work in progress.   
Reach out to [jkowalleck](https://github.com/jkowalleck) to ask for help.


## Backend

It is encouraged to use a [virtual python environment](https://docs.python.org/3/library/venv.html)
via `python -m venv .venv` and activate it afterwards.  
Then install the env tools via `python -m pip install wheel setuptools pip`.

Install the development requirements [requirements/dev.txt](../../requirements/dev.txt) 
via `python -m pip install -r requirements/dev.txt`.

You might also want to install _nichtparasoup_ in developer mode.  
Run `python -m pip install --no-build-isolation --editable .` from the project root.

After writing the code have the code fixed via
[`isort`](https://pypi.org/project/isort/) and
[`autopep3`](https://pypi.org/project/autopep3/).   
These tools are installed via development requirements mentioned earlier.

Do not forget to [test](testing.md) the code.  
This will also check for
import order (fix via `isort`) and
code style (fix via `autopep8`).

## Image crawler

**TODO**
