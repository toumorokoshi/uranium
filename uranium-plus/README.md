# uranium-plus: opinionated usage of uranium

*uranium-plus is an alpha project. use at your own risk, and things are subject to change*

uranium-plus is an opinionated way of using uranium,
relying on standardization to provide functionality out of the box:

* a `uranium test` directive, using pytest
* a `uranium publish` directive, to publish packages
* a `uranium main` directive, 

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
