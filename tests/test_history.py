import os
import pytest
from uranium.history import History
from uranium.exceptions import HistoryException


def test_creates_file(history):
    assert not os.path.exists(history.path)
    history.save()
    assert os.path.exists(history.path)


def test_save_load(history):
    history["foo"] = "bar"
    history.save()

    new_history = History(history.path)
    new_history.load()

    assert history["foo"] == "bar"


def test_no_fail_on_load_no_file(history):
    history.load()


def test_not_able_to_serialize(history):
    import re
    history["unserializable"] = re.compile("foo")
    with pytest.raises(HistoryException):
        history.save()


def test_not_able_to_serialize_subattribute(history):
    import re
    history["unserializable"] = [re.compile("foo")]
    with pytest.raises(HistoryException):
        history.save()

    history["unserializable"] = {"foo": re.compile("foo")}
    with pytest.raises(HistoryException):
        history.save()
