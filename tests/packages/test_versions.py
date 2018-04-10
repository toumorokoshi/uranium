import pytest
from uranium.packages.versions import Versions
from packaging.specifiers import SpecifierSet


@pytest.fixture
def versions():
    return Versions()


def test_versions_coerce_lowercase(versions):
    """
    coerce package names to lowercase
    """
    versions["SQLAlchemy"] = "==1.0.11"
    assert versions["sqlalchemy"] == "==1.0.11"


def test_versions_coerce_lowercase_update(versions):
    """
    coerce package names to lowercase for update.
    """
    versions.update({
        "SQLAlchemy": "==1.0.11"
    })
    assert versions["sqlalchemy"] == "==1.0.11"


def test_versions_coerce_lowercase_get(versions):
    """
    getting a package name should also be lowercase.
    """
    versions.update({
        "SQLAlchemy": "==1.0.11"
    })
    assert versions["SQLAlchemy"] == "==1.0.11"


def test_delete_coerce_lowercase(versions):
    """
    getting a package name should also be lowercase.
    """
    versions.update({
        "SQLAlchemy": "==1.0.11"
    })
    del versions["SQLAlchemy"]


def test_and_operator(versions):
    """
    the and operator should work for dictionaries
    """
    versions["foo"] = ">1.0"
    versions &= {"foo": "<1.1"}
    assert SpecifierSet(versions["foo"]) == SpecifierSet(">1.0,<1.1")
