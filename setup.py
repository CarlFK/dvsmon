# -*- coding: utf-8 -*-
DISTUTILS_DEBUG="True"

from glob import glob
from distutils.core import setup

config = {}

config['classifiers'] = [
			'Development Status :: 4 - Development',
			'Intended Audience :: Video',
			'Natural Language :: English',
			'Operating System :: OS Independent',
			'Programming Language :: Python',
			]


setup(name='dvsmon',
			version='1.0',
			packages=[],
			scripts=['dvs-mon.py'],
			description='GUI to launch and monitor the DVswitch components.',
			author='Carl F. Karsten',
			author_email='carl@personnelware.com',
			maintainer='Carl F. Karsten',
			maintainer_email='carl@personnelware.com',
			license="MIT",
			url='http://dvswitch.alioth.debian.org/wiki/dvsmon/',
			data_files=[
                         ('bin/', ['dvs-mon.py']),
                         ('share/dvsmon/dv', glob("app_data/dv/*")),
                         ('share/pixmaps', ['dvswitch-logo.svg']),
                         ('share/applications/', ["dvsmon.desktop"])
                ],

			**config
			)
