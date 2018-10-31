#! /usr/bin/python3.5

import os
from setuptools import setup, find_packages

DATA_DIR = 'market%sdata' % os.path.sep
setup(name='market',
      version='0.0.1',
      packages=find_packages(),
      data_files=[(DATA_DIR, [os.path.join(DATA_DIR, 'items.json')])],  # FIXME: handle this recursively
      entry_points={
          'console_scripts': [
              'market = market.__main__:main'
          ]
      },
      )
