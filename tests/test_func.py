from . import data
from zero import Function


def test_func():
    print("[test] Testing zero.Function")
    a = Function(data.func)
    b = Function(data.func_bad)
    c = Function(data.func_with_some_sections)
    d = Function(data.func_without_docs)
