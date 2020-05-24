from fjell.config import Config


def test_initial_access():
    c = Config({"foo": "bar"})
    assert c["foo"] == "bar"
    assert c.foo == "bar"


def test_update():
    c = Config({"foo": "old"})
    c["foo"] = "new"
    assert c["foo"] == "new"

    c = Config({"foo": "old"})
    c.foo = "new"
    assert c.foo == "new"

    c = Config({"foo": "old"})
    c.update({"foo": "new"})
    assert c["foo"] == "new"


def test_nested():
    c = Config({"nested": {"foo": "bar"}})
    assert c["nested"]["foo"] == "bar"
    assert c.nested.foo == "bar"
