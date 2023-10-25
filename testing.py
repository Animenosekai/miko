"""Testing AST parsing"""
import ast
import builtins
import dataclasses
import importlib
import inspect
import sys
import typing

from rich.console import Console

import miko


def get_element(dot_path: str, builtin: bool = False) -> typing.Any:
    """
    Get a element from its dot path

    Warning: Keep in mind that the full dot path needs to be provided

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
    # Might be a builtin element ?
    try:
        return getattr(builtins, dot_path)
    except AttributeError:
        pass

    # Might be an element already loaded ?
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
    # Ok, now lets find the module where it was defined
    for element in processing.copy():
        try:
            # Trying to import the whole module again
            result = importlib.import_module(".".join(module
                                                      + [element]))
            # Ok so we have at least this found
            module.append(element)
            processing.pop(0)  # we already processed it
        except Exception:
            # This happens when the we arrive on a non-module element
            # Example: some_module.some_submodule.some_variable
            #          ~~~~~~~~~~~~~~~~~~~~~~~~~~
            #       It should have found all of this
            #                                  but stopped at this
            break

    # Couldn't find any module
    if not result:
        raise ValueError(
            f"Couldn't find the module from the given dot path ({dot_path})")

    # The dot path leads to a module,
    # there is nothing to search further
    if not processing:
        return result

    # Trying to find the element within the module
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
    #  -3    -2    -1    0     1 (shift by -1 * (len1 - len2))
    defaults_length = len(node.args.args) - len(node.args.defaults)
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
    defaults_length = len(node.args.kw_defaults) - len(node.args.kw_defaults)
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


@dataclasses.dataclass
class Element:
    """A documented element"""
    node: ast.AST
    """The node"""
    parents: typing.List[ast.AST] = dataclasses.field(default_factory=list)
    """The nesting where the element was defined"""
    docstring: typing.Optional[ast.Constant] = None
    """The docstring element"""

    @property
    def signature(self) -> typing.Optional[inspect.Signature]:
        """If available, the signature of the node"""
        try:
            return signature_from_ast(self.node)
        except Exception:
            return None

    @property
    def documentation(self) -> miko.Documentation:
        """Returns the documentation for the node"""
        return miko.Documentation(self.docstring.value if self.docstring else "",
                                  signature=self.signature,
                                  noself=True)


def get_elements(node: ast.AST,
                 parents: typing.Optional[typing.List[ast.AST]] = None):
    """
    Gets all of the elements which could be documented inside the AST

    Parameters
    ----------
    node: ast.AST
        The Abstract Syntax Tree element to search into
    """
    parents = parents or []

    results: typing.List[Element] = []
    targets: typing.List[Element] = []  # This holds the last assignements

    for element in ast.iter_child_nodes(node):
        # If we have a straightforward assignement
        # Example: some_var = some_value or some_var = another_var = some_value
        if isinstance(element, ast.Assign):
            targets = []
            for target in element.targets:
                if isinstance(target, ast.Name):
                    # Add each variable name
                    # `element` is added to the parents to conform with
                    # the `ast.AnnAssign` case
                    targets.append(Element(target,
                                           parents=parents + [node, element]))

        # If we have an annotated assignement
        # Example: some_var: some_type = some_value
        if isinstance(element, ast.AnnAssign):
            # We are adding `element` to get to retrieve the
            # annotation when looking into the variable
            targets = [Element(element.target,
                               parents=parents + [node, element])]

        # Constants are inside ast.Expr
        if isinstance(element, ast.Expr):
            element = element.value

        # If we have a constant that is a string
        # coming right after `targets` (assignements)
        if isinstance(element, ast.Constant) and isinstance(element.value, str) and targets:
            # Then we add this element as the docstring of the assignements
            for target in targets:
                target.docstring = element
        elif isinstance(element, (ast.Assign, ast.AnnAssign)):
            # If we are assigning something,
            # we shouldn't get rid of the targets for now
            pass
        else:
            # No docstring was found on the assignements
            # Clear the assignements as anything after that
            # is no longer right after
            targets = []

        if isinstance(element, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.Module)):
            # We have a callable
            # if (element.body
            #     and isinstance(element.body[0], ast.Constant)
            #         and isinstance(element.body[0].value, str)):
            if (element.body
                    and isinstance(element.body[0], ast.Expr)
                    and isinstance(element.body[0].value, ast.Constant)
                    and isinstance(element.body[0].value.value, str)):
                # With the first thing in it being a string (docstring)
                docstring = element.body[0].value
            else:
                docstring = None

            # We are adding the callable element
            adding = [Element(element, parents=parents +
                              [node], docstring=docstring)]
        else:
            # Might be another type of element,
            # which should be documented if and only if
            # the element is inside `targets`
            adding = targets

        # We recursively add the other child elements
        # and the current element
        results.extend(adding
                       + get_elements(element, parents=parents + [node]))

    return results


if __name__ == "__main__":
    c = Console()

    with open("test.py") as f:
        r = ast.parse(f.read())

    c.print(ast.dump(r, indent=4))
    c.print(get_elements(r))
    for element in get_elements(r):
        c.print(element.node.__class__.__name__, "at line", element.node.lineno, ":", element.documentation)

    # for element in ast.iter_child_nodes(r):
    #     c.print(ast.dump(element, indent=4))
