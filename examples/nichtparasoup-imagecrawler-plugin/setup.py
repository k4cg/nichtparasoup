#!/usr/bin/env python3

from setuptools import find_packages, setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='nichtparasoup-imagecrawler-placeholders',
    version='0.0.1',
    description='PlaceholderImages for UI tests',
    python_requires='>=3.5',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*', 'examples']),
    entry_points=dict(
        nichtparasoup_imagecrawler=[
            'DummyImage = nichtparasoup_placeholders:DummyImage',
        ],
    ),
    install_requires=[
        'nichtparasoup',  # you want to pin a min-version ala `>2.2` -  was not done here, since its in-dev example
    ],
    extras_require=dict(
        testing=[
            'mypy',
            'pytest>=5,<5.3.4',  # 5.3.4 has a bug: https://github.com/pytest-dev/pytest/issues/6517
            'coverage',
            'ddt',
        ]
    ),
)
