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
        'nichtparasoup',
        # This example requires `nichtparasoup>=2.3`
        # You SHOULD write the min-version dependency in your real-world.
        # This was not done here, since its an in-dev example.
    ],
    extras_require=dict(
        testing=[
            'mypy>=0.761',
            'pytest>=5.3.5',  # 5.3.4 has a bug: https://github.com/pytest-dev/pytest/issues/6517
            'coverage>=5.0',
            'ddt>=1.2',
        ]
    ),
)
