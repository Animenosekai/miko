from . import data
from miko import Function


def test_func():
    print("[test] Testing miko.Function")
    a = Function(data.func)
    b = Function(data.func_bad)
    c = Function(data.func_with_some_sections)
    d = Function(data.func_without_docs)
