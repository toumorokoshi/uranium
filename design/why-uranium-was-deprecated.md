# Why Uranium Was Deprecated

@toumorokoshi

Officially as of 2021/12/07 (although unofficially probably well before then), this project is deprecated.

This document serves to help provide some context on why the project is no longer being worked on.

Thoughts in this document are my own, and do not reflect the opinion of any other entity.

## Why was Uranium created in the first place?

Uranium came from a need that I had at Zillow Group for a way to package Python applications as a tarball, and to be compatible with some of the sandboxing requirements of [buildout](https://buildout.org/).

A common use case at the time was the need for some custom build directives, and buildout required a process of creating and publishing Python packages to extend a buildout.cfg file. Uranium allowed the authoring of tasks inline the build file itself, and an inheritance system that allowed one to consume scripts easily from common files as necessary. For those situations, it was indeed easier to do this through Uranium.

## Reason 1: The Python packaging ecosystem has evolved

When Uranium was written, sans Buildout, Python's build ecosystem amounted to a setup.py or a requirmeents.txt to manage dependencies. There wasn't a lot of tooling aside from generic ones like Make for helping automate the development workflow or help with things like installing common tools.

Since then, [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) is now a thing, with several PEPs standardizing how to use it, and tools like [Poetry](https://python-poetry.org/) which leverage those primitives well, and also have a dedicated community working on it.

Although I still believe Uranium has some really interesting ideas (arbitrary task creation and easy importing of shared build tooling and configuration), It's no longer unique in resolving the app development and packaging user journey, and certainly not the most well-funded.

## Reason 2: Uranium's relied on internal PyPA package code, which is regularly refactored

One feature that was needed by Zillow was the ability to set version of dependencies proactively, what pip now calls "constraints".

At the time that Uranium was created, constraints were not exposed publicly. In order to replicate this behavior, I had to directly import Pip classes, extend them to inject version resolution behavior to ensure that the versions matched the constraints.

This technique was used for multiple libraries required for packaging to work: the `packaging`, `pip`, `virtualenv` repositories, to name a few.

Over the years, each of these packages have been heavily refactored: I really do appreciate PyPA's rigor around improving their codebase, but it came at the cost of requiring hacks like Uranium to be regularly refactored and find where the old code went, or find another way to patch in the desired behavior.

In addition to my professional priorities changing, the other factor was the major refactor of `virtualenv` to no longer have a one-file `virtualenv.py` which vastly simplified the important and leveraging the code that the module has.