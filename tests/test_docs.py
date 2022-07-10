from . import data
from zero import Docs


def test_docs():
    print("[test] Testing zero.Docs")
    docs = Docs(data.func.__doc__)
    assert docs.description
