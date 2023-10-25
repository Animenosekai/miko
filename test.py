"""
Documenting at the top of the module
"""

# Commenting the imports
import pathlib
import translatepy

CONSTANT = 1
"""Documenting a constant"""


def test(a, b: int, /, c: int = 4, d=5, e: int = 6, *args, f: str, **kwargs) -> translatepy.language.Language:
    """Documenting a function"""

    def inner():
        """Documenting an inner function"""

    local_variable: int = 2
    """Documenting a local variable"""

    local_declaration: int
    """Documenting a local declaration"""

    local_declaration = 3
    """Redeclaration of a variable"""


class Test:
    '''Documenting a class'''

    def __init__(self) -> None:
        """Documenting a method"""


b = translatepy.language.Language("Hello")
