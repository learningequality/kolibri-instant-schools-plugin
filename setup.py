#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import sys

from setuptools import setup


def read_file(fname):
    """
    Read file and decode in py2k
    """
    if sys.version_info < (3,):
        return open(fname).read().decode("utf-8")
    return open(fname).read()


dist_name = 'kolibri_instant_schools_plugin'
plugin_name = 'kolibri_instant_schools_plugin'
repo_url = 'https://github.com/fle-internal/kolibri-instant-schools-plugin'

readme = read_file('README.md')
doclink = """
Documentation
-------------

The full documentation is at."""

# Default description of the distributed package
description = (
    """Kolibri Plugin to provide specific functionality and branding for the Vodafone Instant Schools project"""
)


######################################
# STATIC AND DYNAMIC BUILD SPECIFICS #
######################################

def enable_log_to_stdout(logname):
    """Given a log name, outputs > INFO to stdout."""
    log = logging.getLogger(logname)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    log.addHandler(ch)


setup(
    name=dist_name,
    version="0.3",
    description=description,
    long_description="{readme}\n\n{doclink}".format(
        readme=readme,
        doclink=doclink
    ),
    author='Learning Equality',
    author_email='info@learningequality.org',
    url=repo_url,
    packages=[
        str(plugin_name),  # https://github.com/pypa/setuptools/pull/597
    ],
    package_dir={plugin_name: plugin_name},
    install_requires=["smpplib2>=0.1.1"],
    include_package_data=True,
    license='All Rights Reserved',
    zip_safe=False,
    keywords='kolibri',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: All Rights Reserved',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
