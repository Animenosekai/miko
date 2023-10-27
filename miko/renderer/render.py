import ast

from miko import static


def make_docs(source: str):
    # Recursively make docs for all modules in separate files
    pass


def make_module_docs(element: static.Element[ast.Module]):
    # Recursively make docs for all elements in the module
    pass


def make_class_docs(element: static.Element[ast.ClassDef]):
    # Recursively make docs for all elements in the class
    pass


def make_function_docs(element: static.Element[ast.FunctionDef | ast.AsyncFunctionDef]):
    pass


def make_variable_docs(element: static.Element[ast.Name]):
    pass
