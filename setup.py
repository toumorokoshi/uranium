#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

is_release = False
if "--release" in sys.argv:
    sys.argv.remove("--release")
    is_release = True

base = os.path.dirname(os.path.abspath(__file__))

install_requires = [
    "deepmerge==0.0.3",
    "docopt==0.6.2",
    "pip==9.0.1",
    "requests==2.13.0",
    "setuptools==35.0.1",
    "virtualenv==15.1.0"
]

tests_require = [
    'httpretty',
]

setup(name='uranium',
      setup_requires=["vcver==0.0.8"],
      vcver={"is_release": is_release, "path": base},
      description='a build system for python',
      long_description=open('README.rst').read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@tsutsumi.io',
      url='http://uranium.readthedocs.org',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': [
              'uranium=uranium.main:main'
          ],
      },
      tests_require=tests_require
)
