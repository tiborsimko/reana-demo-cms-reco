# -*- coding: utf-8 -*-
#
# This file is part of reana
# Copyright (C) 2019 CERN.
#
# reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""cms-reco"""

import os
import re

from setuptools import setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
]

extras_require = {
    'docs': [
        'Sphinx>=1.4.4,<2.0',
        'sphinx-rtd-theme>=0.1.9',
        'sphinx-click>=1.0.4',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for key, reqs in extras_require.items():
    if ':' == key[0]:
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'click>=7,<8',
    'cookiecutter>=1.6.0'
]

# Get the version string. Cannot be done with import!
with open(os.path.join('cms_reco', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

setup(
    name='reana-demo-cms-reco',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    author='REANA',
    author_email='info@reana.io',
    url='https://github.com/reanahub/reana-client',
    packages=['cms_reco', ],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cms-reco = cms_reco.cli:cms_reco',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)