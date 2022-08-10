from . import data
from miko import Docs


def test_docs():
    print("[test] Testing miko.Docs")
    docs = Docs(data.func.__doc__)
    assert docs.description
