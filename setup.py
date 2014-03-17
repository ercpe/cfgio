#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='cfgio',
		version='0.1.1',
		description='Python library for reading and writing configuration file formats found on a *nix system',
		author='Johann Schmitz',
		author_email='johann@j-schmitz.net',
		url='https://github.com/ercpe/cfgio',
		packages=['cfgio', 'cfgio.specialized'],
		package_dir={'': 'src'},
)