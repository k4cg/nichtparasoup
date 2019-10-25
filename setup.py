from functools import reduce

from nichtparasoup import __version__

REQUIREMENTS = dict(
    config=["yamale"],
    core=[],
    imagecrawler=[],
    webserver=["werkzeug"],
)

SETUP = dict(
    name="nichtparasoup",
    version=__version__,  # use setuptools-scm ?
    license="MIT",
    setup_requires=["setuptools"],
    packages=["nichtparasoup"],
    package_data=dict(
        nichtparasoup=[
            # TODO: check if this is done right. are the files included in dist
            "webserver/htdocs",
            "config/*.yaml",
        ],
    ),
    python_requires=">=3.5",
    install_requires=reduce(lambda r1, r2: r1 + r2, REQUIREMENTS.values(), []),
    extras_require=dict(
        development=[
            "tox",
            "isort",
        ],
        testing=[
            "flake8",
            'flake8-annotations;python_version>="3.6"',
            'flake8-bugbear',
            "flake8-isort",
            'flake8-pep3101',
            "pep8-naming",
            "mypy",
            "coverage",
            "pytest",
            "ddt",
            "yamale",
        ],
    ),
)

if __name__ == "__main__":
    import setuptools
    setuptools.setup(**SETUP)
