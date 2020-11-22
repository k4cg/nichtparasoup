# Style

Code style is checked via flake8 and some plugins.

To have the code styled properly, simply run the following:

```shell script
# run from project root
python -m pip install -r requirements/dev.txt
python -m autopep8 --recursive --in-place .
python -m isort .
```
