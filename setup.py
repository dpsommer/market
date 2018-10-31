#! /usr/bin/python3.5

import os
from setuptools import setup, find_packages

DATA_DIR = 'market%sdata' % os.path.sep
PICKLE_EXTENSION = '.p'

data_files = [f for dir_path, dir_name, file_names in os.walk(DATA_DIR) for f in file_names]
pickle_files = [os.path.join(DATA_DIR, f) for f in filter(lambda x: x.endswith(PICKLE_EXTENSION), data_files)]

setup(name='market',
      version='0.0.1',
      packages=find_packages(),
      data_files=[(DATA_DIR, pickle_files)],
      entry_points={
          'console_scripts': [
              'market = market.__main__:main'
          ]
      },
      )
