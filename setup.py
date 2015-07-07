#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'setuptools==18.0.1',
    'docopt==0.6.2',
    'jinja2==2.7.3',
    'pip==7.1.0',
    'requests==2.7.0',
    'six==1.9.0',
    'virtualenv==13.1.0',
    # we need these two for
    # buildout compatibilty purposes.
    'zc.buildout'
]

tests_require = [
    'httpretty',
    'nose',
]

setup(name='uranium',
      version='0.1.0',
      description='a build system for python',
      long_description='a build system for python',
      author='Yusuke Tsutsumi',
      author_email='yusuke@yusuketsutsumi.com',
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
              'uranium=uranium:main'
          ],
          'uranium.plugin': [
              'default = uranium.example_plugin:ExamplePlugin'
          ]
      },
      tests_require=tests_require
)
