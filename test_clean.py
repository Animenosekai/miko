"""
Documenting at the top of the module
"""
# Commenting the imports
import pathlib

import miko.parsers

CONSTANT = 1
'Documenting a constant'


def test(a: int, b: int, /, c: int = 4, d=5, e: int = 6, *args, f: str, **kwargs) -> int:
    """
    Documenting a function

    Parameters
    ----------
    a: int, deprecated
        Hey
    b: int
    c: int, default = 4
    d: default = 5
    e: int, default = 6
    args
    f: str
    kwargs

    Returns
    -------
    int
    """

    def inner():
        """
        Documenting an inner function

        Note: This is a cool function
        """

    def inner2(a: int) -> str:
        """
        Parameters
        ----------
        a: int

        Returns
        -------
        str
        """
        return str(a)
    local_variable: int = 2
    'Documenting a local variable'
    local_declaration: int
    'Documenting a local declaration'
    local_declaration = 3
    'Redeclaration of a variable'
    return local_declaration


class Test:
    """Documenting a class"""

    def __init__(self) -> None:
        """Documenting a method"""


b: int
'! DEPRECATED'
