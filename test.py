"""
Documenting at the top of the module
"""
# Commenting the imports
import pathlib

import miko.parsers as p
from miko.parsers import important
from miko.parsers.important import Important

MY_NEW_CONSTANT = 1
"""
! DEPRECATED

Documenting a constant

Warning: This is a warning

This is a very important task

Important: This is important

Example: print(MY_NEW_CONSTANT)

Example
-------
>>> from test import MY_NEW_CONSTANT
>>> print(MY_NEW_CONSTANT)

Copyright
---------
Animenosekai: MIT License, year = 2021
    Worked on it
Hey: from = 2021, to = 2023
    Worked again on it

Changelog
---------
2.0
    Became deprecated, use `new_func` instead
1.4
    New default string
0.6
    Raises ImportError instead of RuntimeError
"""


def test(a: int, b: int, /, c: int = 4, d=5, e: int = 6, *args, f: str, **kwargs) -> int:
    """
    Documenting a function

    ! DEPRECATED

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
