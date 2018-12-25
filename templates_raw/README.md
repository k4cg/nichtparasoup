# template builder for UI

This is just the template builder - not needed to run __nichtparasoup__.

## idea

To have proper IDE support when it comes to writing the UI, the thing should be written in several raw files and be
yuiCompressed and put together at the end.
Furthermore it would be great to be able to develop the UI without running __nichtparasoup__.

## requirements

```sh
git submodule update --init --recursive
```

for further information: see the `README` of the submodules

## how to use

just run the `build.sh` so the `templates.py` of __nichtparasoup__ will be built automatically

## attention: symlinks

some files are symlinked - so be sure your environment supports symlinks, otherwise the outcome may be broken.
this is the case on most windows systems.
