#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

install_requires = [
    'docopt>=0.6.2',
    'jinja2',
    'pip>=6',
    'pyyaml',
    'requests',
    'six',
    'virtualenv>=1.11.6',
    'zc.buildout'
]

tests_require = [
    'httpretty',
    'nose',
]

setup(name='uranium',
      version='0.0.24',
      description='a build system for python',
      long_description='a build system for python',
      author='Yusuke Tsutsumi',
      author_email='yusuke@yusuketsutsumi.com',
      url='http://toumorokoshi.github.io/uranium',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 1 - Planning',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3'
      ],
      entry_points={
          'console_scripts': [
              'uranium=uranium:main'
          ]
      },
      tests_require=tests_require
)
