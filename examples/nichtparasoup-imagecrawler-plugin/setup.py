#!/usr/bin/env python3

from setuptools import find_packages, setup

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
        'nichtparasoup>=2.2',
    ],
    extras_require=dict(
        testing=[
            'mypy',
            'pytest',
            'coverage',
        ]
    ),
)
