# Development

_TODO_

This documentation is work in progress.   
Reach out to [jkowalleck](https://github.com/jkowalleck) to ask for help.


## Backend

Install the development requirements from [requirements/dev.txt](../../../requirements/dev.txt) via `pip`.

You might also want to install _nichtparasoup_ in developer mode.  
Run `pip install --no-build-isolation --editable .` from the project root.

After writing the code have the code fixed via
[`isort`](https://pypi.org/project/isort/) and
[`autopep3`](https://pypi.org/project/autopep3/).   
These tools are installed via development requirements mentioned earlier.

Do not forget to [test](testing.md) the code.  
This will also check for
import order (fix via `isort`) and
code style (fix via `autopep8`).

## Image crawler

_TODO_


## Frontend

See [web-ui development docs](../web-ui/index.md)
