import ast
import builtins
import importlib
import inspect
import sys
import typing

from rich.console import Console

c = Console()

with open("test.py") as f:
    r = ast.parse(f.read())

c.print(ast.dump(r, indent=4))

for element in ast.iter_child_nodes(r):
    c.print(ast.dump(element, indent=4))


def get_element(dot_path: str, builtin: bool = False) -> typing.Any:
    """
    Get a element from its dot path

    Parameters
    ----------
    dot_path: str
        The dot path of the element to get
    builtin: bool, default = False
        If the element should be already loaded or coming from a builtin module.
        This avoids loading unknown code, which could lead to unexpected results.

    Returns
    -------
    Any
        Any element pointed by the dot path
    """
    try:
        return getattr(builtins, dot_path)
    except AttributeError:
        pass

    try:
        return globals()[dot_path]
    except KeyError:
        pass

    processing = dot_path.split(".")
    if builtin and processing[0] not in sys.stdlib_module_names:
        raise ValueError(
            f"The dot path ({dot_path}) does not seem to point to a builtin element")

    module = []
    result = None
    for element in processing.copy():
        try:
            result = importlib.import_module(".".join(module
                                                      + [element]))
            module.append(element)
            processing.pop(0)
        except Exception:
            break

    if not result:
        raise ValueError(
            f"Couldn't find the module from the given dot path ({dot_path})")

    if not processing:
        return result

    for element in processing:
        result = getattr(result, element)

    return result


def get_dot_path(attr: ast.Attribute | ast.Name) -> str:
    """
    Returns the dot path for a given attribute

    Parameters
    ----------
    attr: ast.Attribute
        The attribute to get the whole dot path from

    Returns
    -------
    str
        The dot path
    """
    if isinstance(attr, ast.Name):
        return attr.id
    if not isinstance(attr, ast.Attribute):
        raise ValueError(
            f"The attribute `{attr}` doesn't seem to be providing enough information to generate the dot path")
    return f"{get_dot_path(attr.value)}.{attr.attr}"


def get_value(expr: typing.Optional[ast.expr], builtin: bool = False) -> typing.Optional[str]:
    """
    Returns the correct value from the given expression

    Parameters
    ----------
    expr: ast.expr, optional
        The expression to get the value from
    builtin: bool, default = False
        If the element should be already loaded or coming from a builtin module
        to be fully loaded. Otherwise a dot path will be returned.
        See `get_element` for more information on loading arbitrary elements.

    Returns
    -------
    str
        The value for the expression
    None
        If it couldn't get the value
    """
    if isinstance(expr, ast.Constant):
        # This happens when the value is defined
        # as a string (ex: lazy loading reference)
        # new_var: "some_type" = ...
        #           ~~~~~~~~~
        # def (...) -> "some_type"
        #               ~~~~~~~~~
        return expr.value
    if isinstance(expr, ast.Name):
        # This happens when the value is defined as a type
        # new_var: some_type = ...
        #          ~~~~~~~~~
        # def (...) -> some_type
        #              ~~~~~~~~~
        result = expr.id
        try:
            return get_element(result, builtin=builtin)
        except (AttributeError, ValueError):
            return result  # should not be a builtin
    if isinstance(expr, ast.Attribute):
        # This happens when the value is defined as
        # an element of something else
        # new_var: some_module.some_var = ...
        #          ~~~~~~~~~~~~~~~~~~~~
        # def (...) -> some_module.some_var
        #              ~~~~~~~~~~~~~~~~~~~~
        result = get_dot_path(expr)
        try:
            return get_element(result, builtin=builtin)
        except (AttributeError, ValueError):
            return result  # should not be a builtin
    return None


def signature_from_ast(node: ast.AsyncFunctionDef | ast.FunctionDef) -> inspect.Signature:
    """
    Computes the signature of a function from its AST

    Parameters
    ----------
    node: ast.AsyncFunctionDef | ast.FunctionDef
        The node to get the signature from

    Returns
    -------
    inspect.Signature
        This the signature of the function,
        retrieved without ever running the code
    """

    # Handling Parameters
    parameters = []

    # Handling Positional Only Args
    # Example: (a, b, /, c) -> Any
    #           ↑  ↑
    for arg in node.args.posonlyargs:
        parameters.append(inspect.Parameter(name=arg.arg,
                          annotation=get_value(
                              arg.annotation) or inspect.Parameter.empty,
                          kind=inspect.Parameter.POSITIONAL_ONLY,
                          default=inspect.Parameter.empty))

    # Handling Positional or Keyword Args
    # Example: (a, b, c) -> Any
    #           ↑  ↑  ↑

    # [arg1, arg2, arg3, arg4, arg5] => len1 == 5
    # [                  def1, def2] => len2 == 2
    #  0   , 1   , 2   , 3   , 4
    #  -3    -2    -1    0     1 (shift by -1 * (len2 + 1))
    defaults_length = len(node.args.defaults) + 1
    for index, arg in enumerate(node.args.args):
        ind = index - defaults_length
        default = inspect.Parameter.empty
        if ind >= 0:
            default_wrapper = node.args.defaults[ind]
            if isinstance(default_wrapper, ast.Constant):
                default = default_wrapper.value

        parameters.append(inspect.Parameter(name=arg.arg,
                                            annotation=get_value(
                                                arg.annotation) or inspect.Parameter.empty,
                                            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                            default=default))

    # Handling Variadic Positional Args
    # Example: (*args) -> Any
    if node.args.vararg:
        parameters.append(inspect.Parameter(name=node.args.vararg.arg,
                                            kind=inspect.Parameter.VAR_POSITIONAL))

    # Handling Keyword Only Args
    # Example: (a, b, *, c) -> Any
    #                    ↑
    defaults_length = len(node.args.kw_defaults) + 1
    for index, arg in enumerate(node.args.kwonlyargs):
        ind = index - defaults_length
        default = inspect.Parameter.empty
        if ind >= 0:
            default_wrapper = node.args.kw_defaults[ind]
            if isinstance(default_wrapper, ast.Constant):
                default = default_wrapper.value

        parameters.append(inspect.Parameter(name=arg.arg,
                                            annotation=get_value(
                                                arg.annotation) or inspect.Parameter.empty,
                                            kind=inspect.Parameter.KEYWORD_ONLY,
                                            default=default))

    # Handling Variadic Keyword Args
    # Example: (**kwargs) -> Any
    if node.args.kwarg:
        parameters.append(inspect.Parameter(name=node.args.kwarg.arg,
                                            kind=inspect.Parameter.VAR_KEYWORD))

    # Handling the Return Annotation
    returned = get_value(node.returns) or inspect.Signature.empty

    return inspect.Signature(parameters=parameters, return_annotation=returned)


for element in ast.walk(r):
    if isinstance(element, ast.AsyncFunctionDef | ast.FunctionDef):
        print(signature_from_ast(element))
