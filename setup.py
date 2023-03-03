#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='chexmix',
    version='0.0.1',
    description='Mix them all and have something good',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.md'))
    ),
    author='Bionsight',
    author_email='dev@bionsight.com',
    url='https://github.com/bionsight/chexmix',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Private :: Do Not Upload',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/bionsight/chexmix/issues',
    },
    keywords=[
        'data',
    ],
    python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    install_requires=[
        'biopython',
        'chembl_webresource_client',
        'click',
        'lxml',
        'networkx',
        'pandas',
        'python-dotenv',
        'requests',
        'tqdm',
        'xmlschema'
    ],
    tests_require=[
        'coverage',
        'pytest',
    ],
    extras_require={
        'interactive': [
            'matplotlib',
            'jupyterlab',
            'ipywidgets'
        ],
    }
)
