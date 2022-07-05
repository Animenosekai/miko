def func():
    """
    !DEPRECATED!

    Hello, this is a description

    Parameters
    ----------
    a: bool
        this is the first argument
    b: int | float, default = 1.2
        this is the second argument
    c: str, optional
        this is the third argument
        it can have multiple lines
    d: str, deprecated
    e: float, deprecated, default = 1.2
        a deprecated argument

    Returns
    -------
    int
        the number returned
    str
        if it is a string returned
    list[int, str]
        if it's a list of both
    translatepy.Language
        using dot notation

    Example
    -------
    >>> func()
    "It is false"
    >>> func(True)
    "It is true"
    # when using something other than a boolean
    >>> func(1)
    2

    Raises
    ------
    ValueError
        If there is an error with the value
    InputError
        If there is an error with the value

    Raises
    ------
    RuntimeError
        If there is an error with the value

    Warning: This is a serious warning

    ...description...

    Warning: Another warning

    Note: Yup, that's true

    ...description...

    Note: Another note

    Changelog
    ---------
    1.4
        New default string
    0.6
        Raises ImportError instead of RuntimeError

    Copyright
    ---------
    Animenosekai
        The initial author
    Some other dev
        A very cool collaborator

    But this is also part of the description
    """
    pass

def func_bad():
    """
        ! deprecated ! hellooooo

    Hello, this is a description

    Parameter
    -----
    a: bool
        this is the first argument
    b:int|float, default =1.2
      this is the second argument
    c : str, optional
        this is the third argument
        it can have multiple lines
    d: str, deprecated
    e: float, deprecated, default = 1.2
        a deprecated argument

    Returning
    -----
    int
        the number returned
    str
        if it is a string returned
    list[int, str]
        if it's a list of both
    translatepy.Language
        using dot notation

    Example
    -------
    >>> func()
    "It is false"
    >>> func(True)
    "It is true"
    # when using something other than a boolean
    >>> func(1)
    2

    Errors
    ------
    ValueError
        If there is an error with the value
    InputError
        If there is an error with the value

    Exception
    ------
    RuntimeError
        If there is an error with the value

    Warning :This is a serious warning

    ...description...

    Warning: Another warning

    Note : Yup, that's true

    ...description...

    Note: Another note

    Changelog
    ---------
    1.4
        New default string
    0.6
        Raises ImportError instead of RuntimeError

    Copyright
    ---------
    Animenosekai
        The initial author
    Some other dev
        A very cool collaborator

    But this is also part of the description
    """
    pass


def func_without_docs(a: int, b: str = "hello") -> float:
    return 1.2
