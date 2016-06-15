#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    "docopt==0.6.2",
    "pip==8.1.2",
    "requests==2.9.1",
    "setuptools==21.2.1",
    "virtualenv==15.0.2"
]

tests_require = [
    'httpretty',
]

setup(name='uranium',
      version='0.2.36b',
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
              'uranium=uranium.scripts.main:main'
          ],
      },
      tests_require=tests_require
)
