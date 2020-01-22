# uranium-plus: opinionated usage of uranium

*uranium-plus is an alpha project. use at your own risk, and things are subject to change*

uranium-plus is an opinionated way of using uranium,
relying on standardization to provide functionality out of the box:

* a `uranium test` directive, using pytest
* a `uranium publish` directive, to publish packages
* a `uranium main` directive, 

## standard conventions

* your tests live in either in a "tests" directory under your main module.
* a setup.py file is used to declare your package


## using uranium-plus in your ubuild.py

You can install uranium-plus, then call the provided boostrap function to bootstrap your repo. from that point on,
you will have all the standard uranium-plus goodies:

    # ubuild.py
    build.packages.install("uranium-plus")
    import uranium_plus

    build.config.update({
        "uranium-plus": {
            "module": "my-module"
        }
    })

    uranium_plus.bootstrap(build)


## Using uranium-plus for vscode

uranium-plus includes built in configuration for
maximum compatibility with vscode's vscode-python extension.

modify your uranium-plus installation to include the vscode extras:

    # ubuild.py
    build.packages.install("uranium-plus[vscode]")
    import uranium_plus

## Design / Best Practices

uranium-plus ensures best practices that are not necessarily enforced by uranium
itself, this inclues:

### Installing all dependencies and requirements during the main() call.

Developers may go offline at inopportune times. As a result, there should not
be surprise dependencies that are discovered only when the task is invoked for the 
first time.

uranium-plus moves almost all dependencies to the setup.py, and moves dependencies
that can only be resolved by user configuration (such as test.packages) to the main()
function to be installed then.