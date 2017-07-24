import pytest
from uranium.exceptions import PackageException
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


def test_create_args_includes_install_options():
    args = _create_args("pytest",
                        install_options=["--prefix=/opt/srv",
                                         "--install-lib=/opt/srv/lib"])
    assert args == [
        "--install-option", "--prefix=/opt/srv",
        "--install-option", "--install-lib=/opt/srv/lib",
        "pytest"
    ]


def test_create_args_raises_on_invalid_version():
    with pytest.raises(PackageException) as exc:
        _create_args("pytest", version="3.1.3")
    assert "Invalid version specifier" in str(exc)


def test_create_args_accepts_valid_version():
    args = _create_args("pytest", version=">=3.1.3")
    assert args == ["pytest>=3.1.3"]
