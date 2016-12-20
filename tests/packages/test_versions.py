import pytest
from uranium.packages.versions import Versions


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
