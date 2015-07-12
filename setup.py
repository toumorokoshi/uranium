#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = []

tests_require = [
    'httpretty',
]

setup(name='uranium',
      version='0.2.5',
      description='a build system for python',
      long_description='a build system for python',
      author='Yusuke Tsutsumi',
      author_email='yusuke@tsutsumi.io',
      url='http://uranium.readthedocs.org',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      entry_points={
          'console_scripts': [
              'uranium=uranium.scripts.uranium:main'
          ],
      },
      tests_require=tests_require
)
