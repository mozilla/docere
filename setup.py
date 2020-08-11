#!/usr/bin/env python
from setuptools import setup, find_packages

test_deps = [
    'coverage',
    'pytest-cov',
    'pytest-timeout',
    'pytest',
]

extras = {
    'testing': test_deps,
}

setup(
    name='docere',
    version='0.9',
    description='Tools for publishing analyses as a static site',
    author='Ryan Harter',
    author_email='harterrt@mozilla.com',
    url='https://github.com/harterrt/docere.git',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'docere = docere.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=[
        'jinja2',
        'click',
    ],
    tests_require=test_deps,
    extras_require=extras,
)
