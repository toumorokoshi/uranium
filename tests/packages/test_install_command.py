from uranium.packages.install_command import _create_args


def test_create_args_includes_trusted_hosts():
    """
    if index urls are passed in, there should be a trusted host
    argument returned.
    """
    args = _create_args("pytest", index_urls=["http://pypi.python.org/simple",
                                              "http://pypi2.python.org/simple"])
    assert args == [
        "-i", "http://pypi.python.org/simple",
        "--trusted-host", "pypi.python.org",
        "--extra-index-url", "http://pypi2.python.org/simple",
        "--trusted-host", "pypi2.python.org",
        "pytest"
    ]
