from . import data
from zero import Docs


def test_docs():
    docs = Docs(data.func)
    assert docs.description
