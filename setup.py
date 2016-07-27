#!/usr/bin/env python

from distutils.core import setup

setup(name='pykodi',
      version='0.3.2',
      description='Python Distribution Utilities',
      author='Arnaud Bertrand',
      author_email='rnd.bertrand@gmail.com',
      url='https://github.com/Arn-O/py-kodi-remote-controller',
      packages=[
        'pykodi',
        'pykodi.core',
        'pykodi.display',
        'pykodi.echonest',
        'pykodi.rpc'
      ],
      install_requires=[
        'progressbar'
      ]
     )
