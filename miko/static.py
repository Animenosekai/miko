"""
Implementation of miko's static code analysis tools

This is used to retrieve information on the different elements of the code
without having to run it.
"""
import builtins
import dataclasses
import importlib
import importlib.util
import inspect
import pathlib
import sys
import typing

from importlib.machinery import PathFinder

import ast_comments as ast
if typing.TYPE_CHECKING:
    import ast
import autopep8
import isort

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


def signature_from_ast(node: ast.AsyncFunctionDef | ast.FunctionDef, builtin: bool = False) -> inspect.Signature:
    """
    Computes the signature of a function from its AST

    Parameters
    ----------
    node: ast.AsyncFunctionDef | ast.FunctionDef
        The node to get the signature from
    builtin: bool, default = False
        If annotations should be already loaded or
        coming from a builtin module to be fully loaded.
        Otherwise a dot path will be returned.
        See get_element for more information on loading arbitrary elements.

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
                          annotation=(get_value(arg.annotation, builtin=builtin)
                                      or inspect.Parameter.empty),
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
                                            annotation=(get_value(arg.annotation, builtin=builtin)
                                                        or inspect.Parameter.empty),
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
                                            annotation=(get_value(arg.annotation, builtin=builtin)
                                                        or inspect.Parameter.empty),
                                            kind=inspect.Parameter.KEYWORD_ONLY,
                                            default=default))

    # Handling Variadic Keyword Args
    # Example: (**kwargs) -> Any
    if node.args.kwarg:
        parameters.append(inspect.Parameter(name=node.args.kwarg.arg,
                                            kind=inspect.Parameter.VAR_KEYWORD))

    # Handling the Return Annotation
    returned = get_value(node.returns,
                         builtin=builtin) or inspect.Signature.empty

    return inspect.Signature(parameters=parameters, return_annotation=returned)


def export_node(node: ast.AST) -> typing.Dict[str, typing.Any]:
    """Exports the data of an AST node"""
    return {
        "type": node.__class__.__name__,
        "start": {
            "line": node.lineno if hasattr(node, "lineno") else None,
            "column": node.col_offset if hasattr(node, "col_offset") else None
        },
        "end": {
            "line": node.end_lineno if hasattr(node, "end_lineno") else None,
            "column": node.end_col_offset if hasattr(node, "end_col_offset") else None
        }
    }


NodeType = typing.TypeVar("NodeType", bound=ast.AST)


@dataclasses.dataclass
class Element(typing.Generic[NodeType]):
    """A documented element"""
    node: NodeType
    """The node"""
    parents: typing.List[ast.AST] = dataclasses.field(default_factory=list)
    """The nesting where the element was defined"""
    docstring: typing.Optional[ast.Constant] = None
    """The docstring element"""

    safe_annotations: bool = False
    """If the annotations should be safely loaded"""

    @property
    def signature(self) -> typing.Optional[inspect.Signature]:
        """If available, the signature of the node"""
        try:
            return signature_from_ast(self.node, builtin=self.safe_annotations)
        except Exception:
            return None

    def document(self, **kwargs):
        """Documents the element"""
        return miko.Documentation(self.docstring.value if self.docstring else "",
                                  signature=self.signature,
                                  **kwargs)

    @property
    def documentation(self):
        """Returns the documentation for the node"""
        return self.document()

    def export(self, indent: int = 4, **kwargs):
        """Exports the data"""
        docs = self.document(**kwargs)
        return {
            "node": export_node(self.node),
            "parents": [
                export_node(parent)
                for parent in self.parents
            ],
            "documentation": docs.exported,
            "docstring": docs.dumps(indent=indent)
        }

    @property
    def exported(self):
        """Exported data"""
        return self.export()


@dataclasses.dataclass
class ConstantElement(Element[ast.Name | ast.Module]):
    """A constant element"""
    # node: ast.Name | ast.Attribute | ast.Subscript

    def document(self, **kwargs):
        """Documents the element"""
        return miko.ConstantDocumentation(self.docstring.value
                                          if self.docstring else "", **kwargs)

    @property
    def documentation(self):
        return self.document()


def get_elements(node: ast.AST,
                 parents: typing.Optional[typing.List[ast.AST]] = None,
                 safe_annotations: bool = False):
    """
    Gets all of the elements which could be documented inside the AST

    Parameters
    ----------
    node: ast.AST
        The Abstract Syntax Tree element to search into
    parents: typing.Optional[typing.List[ast.AST]], default = None
        The parents of the current element
    safe_annotations: bool, default = False
        If the annotations should be safely loaded
    """
    parents = parents or []

    results: typing.List[Element] = []
    targets: typing.List[Element] = []  # This holds the last assignements

    def child_nodes():
        """The child nodes"""
        # We are adding the parent node because it is not processed by any parent
        if not parents:
            yield node

        yield from ast.iter_child_nodes(node)

    if len(parents) >= 2:
        if parents[0] == parents[1]:
            parents = parents[1:]

    for element in child_nodes():
        # If we have a straightforward assignement
        # Example: some_var = some_value or some_var = another_var = some_value
        if isinstance(element, ast.Assign):
            targets = []
            for target in element.targets:
                if isinstance(target, ast.Name):
                    # Add each variable name
                    # `element` is added to the parents to conform with
                    # the `ast.AnnAssign` case
                    if parents and parents[-1] != node:
                        adding_parents = parents + [node, element]
                    else:
                        adding_parents = parents + [element]
                    targets.append(ConstantElement(target,
                                                   parents=adding_parents,
                                                   safe_annotations=safe_annotations))

        # If we have an annotated assignement
        # Example: some_var: some_type = some_value
        if isinstance(element, ast.AnnAssign):
            # We are adding `element` to get to retrieve the
            # annotation when looking into the variable
            if parents and parents[-1] != node:
                adding_parents = parents + [node, element]
            else:
                adding_parents = parents + [element]
            targets = [ConstantElement(element.target,
                                       parents=adding_parents,
                                       safe_annotations=safe_annotations)]

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
            if (element.body
                    and isinstance(element.body[0], ast.Expr)
                    and isinstance(element.body[0].value, ast.Constant)
                    and isinstance(element.body[0].value.value, str)):
                # With the first thing in it being a string (docstring)
                docstring = element.body[0].value
            else:
                docstring = None

            # We are adding the callable element
            if parents and parents[-1] != node:
                adding_parents = parents + [node]
            else:
                adding_parents = parents

            adding: typing.List[Element]

            if isinstance(element, ast.Module):
                adding = [ConstantElement(element, parents=adding_parents,
                                          docstring=docstring,
                                          safe_annotations=safe_annotations)]
            else:
                adding = [Element(element, parents=adding_parents,
                                  docstring=docstring,
                                  safe_annotations=safe_annotations)]

        else:
            # Might be another type of element,
            # which should be documented if and only if
            # the element is inside `targets`
            # adding = targets
            adding = targets

        # We recursively add the other child elements
        # and the current element
        results.extend(adding
                       + get_elements(element, parents=parents + [node],
                                      safe_annotations=safe_annotations))

    # Filtering out duplicates
    output = []
    nodes = []
    for result in results:
        if result.node in nodes:
            continue
        output.append(result)
        nodes.append(result.node)
    return output


def clean_elements(elements: typing.List[Element], indent: int = 4, **kwargs):
    """Cleans up the given elements"""
    for element in elements:
        if (not element.docstring
            and element.signature
                and isinstance(element.node, ast.AsyncFunctionDef | ast.FunctionDef)):
            new_expr = ast.Expr()
            new_expr.value = ast.Constant()
            new_expr.value.value = ""
            new_expr.value.col_offset = element.node.col_offset + indent
            element.node.body.insert(0, new_expr)
            element.docstring = new_expr.value

        if not element.docstring:
            continue

        result = element.document(**kwargs).dumps(indent=indent)

        padding = " " * element.docstring.col_offset

        # We want the right indentation
        results = []
        for line in result.splitlines():
            results.append(padding + line)

        result = "\n".join(results).strip().strip("\n")

        # If this is a multi-line docstring
        # we want to add a newline before
        # and after the docstring
        if "\n" in result:
            result = f"""\n{padding}{result}\n{padding}"""

        if element.docstring:
            element.docstring.value = result
        elif element.signature and isinstance(element.node, ast.AsyncFunctionDef | ast.FunctionDef):
            new_expr = ast.Expr()
            new_expr.value = ast.Constant()
            new_expr.value.value = result
            element.node.body.insert(0, new_expr)

    return elements


def clean(source: str, indent: int = 4, safe_annotations: bool = False, **kwargs) -> str:
    """Cleans up the source code"""
    tree = ast.parse(str(source))
    elements = get_elements(tree, safe_annotations=safe_annotations)
    clean_elements(elements, indent=indent, **kwargs)
    ast.fix_missing_locations(tree)
    result = ast.unparse(tree)
    result = autopep8.fix_code(result)
    return isort.code(result)


def info(source: str, indent: int = 4, safe_annotations: bool = False, **kwargs) -> typing.List[typing.Dict[str, typing.Any]]:
    """Gathers information on the different elements of the source code"""
    tree = ast.parse(str(source))
    elements = get_elements(tree, safe_annotations=safe_annotations)
    return [
        element.export(indent=indent, **kwargs)
        for element in elements
    ]


@dataclasses.dataclass
class ImportLocation:
    """The location of an import"""
    file: pathlib.Path
    """The file where the import is located"""
    name: str
    """
    The name of the import.
    This is the name of the variable where the import is stored.

    Example
    -------
    >>> import x
    # name == "x"
    >>> import x.y
    # name == "x.y"
    >>> from x import y
    # name == "y"
    >>> from w.x import y as z
    # name == "z"
    """
    node: ast.Import | ast.ImportFrom
    """The node of the import, used to retrieve the location within the file"""


PYTHON_EXTENSIONS = (".py", ".pyw", ".pyc", ".pyo")


@dataclasses.dataclass
class Import:
    """An import"""
    file: pathlib.Path
    """The file which is imported"""
    locations: typing.List[ImportLocation] = dataclasses.field(
        default_factory=list)
    """The locations of the import"""


IMPORTS_CACHE: typing.Dict[str, pathlib.Path] = {}


def resolve_import(name: str, module: typing.Optional[str] = None, level: int = 0,
                   safe: bool = True, context: typing.Optional[pathlib.Path] = None) -> pathlib.Path:
    """
    Resolves an import

    Parameters
    ----------
    name: str
        The name of the import
    module: Optional[str], default = None
        The module of the import
    level: int, default = 0
        The level of the import
    safe: bool, default = True
        Whether to use the safe method of resolving imports
        or the unsafe method of resolving imports
    """
    full_name = ".".join(str(element)
                         for element in [module, name]
                         if element)

    cache_key = full_name + str(level) + str(context) + str(safe)

    if level:
        if not context:
            raise ValueError("Cannot resolve relative import without context")

        context = pathlib.Path(context).resolve()
        for _ in range(level - 1):
            context = context.parent
    else:
        context = None

    result = IMPORTS_CACHE.get(cache_key)
    if result:
        return result

    modules = full_name.split(".")
    last = modules.pop()

    # We now have two choice of how to resolve the import:
    # 1. Use importlib.util.find_spec
    # 2. Try to find the module ourselves

    # If the first option is chosen (i.e. safe is False),
    # and we are trying to find a submodule, importlib will
    # run the parent modules.

    # If the second option is chosen (i.e. safe is True),
    # we will try to find the module ourselves, but this
    # might not be as reliable, because we are not Python.
    # (actually it might work better in some cases, because
    # I still don't know how to fully use importlib.util.find_spec)

    if not safe:
        # Not even sure if that's the correct way of importlib
        # I suspect there is a problem with relative imports since
        # this gives back less results than the "safer" method

        # Might remove later
        try:
            spec = importlib.util.find_spec(("." * level)
                                            + ".".join(modules + [last]))
        except ModuleNotFoundError:
            # The last part might not be a module
            spec = importlib.util.find_spec(("." * level) + ".".join(modules))

        if not spec or not spec.origin:
            raise ImportError(f"Could not find module {full_name}")

        result = pathlib.Path(spec.origin)

        if not result.is_file():
            if spec.origin == "frozen":
                raise ImportError(
                    "Cannot import from frozen module (Most likely a built-in module)")

            raise ImportError("The module is from a non-file source")

        IMPORTS_CACHE[cache_key] = result
        return result

    if context:
        locations = [context]
    else:
        if not modules:
            root_spec = PathFinder.find_spec(last)
            if not root_spec:
                raise ImportError(f"Couldn't find module '{last}'")

            if not root_spec.origin or not pathlib.Path(root_spec.origin).is_file():
                raise ImportError(f"Couldn't find module '{last}'")
            return pathlib.Path(root_spec.origin)
        else:
            root = modules.pop(0)
            root_spec = PathFinder.find_spec(root)

            if not root_spec:
                raise ImportError(f"Couldn't find module '{root}'")

            locations = root_spec.submodule_search_locations

    for parent in locations:
        current = pathlib.Path(parent) / pathlib.Path(*modules)
        # print(full_name, current)
        if current.is_dir():
            # some_module.some_submodule.some_subsubmodule
            # => Here some_module/some_submodule might be a directory
            # => with some_module/some_submodule/__init__.py* being a file
            # => and some_module/some_submodule/subsubmodule.py* being a file
            # => but some_module/some_submodule/subsubmodule might be a directory
            # => and some_module/some_submodule/subsubmodule/__init__.py* might be a file
            for ext in PYTHON_EXTENSIONS:
                if (current / last / "__init__").with_suffix(ext).is_file():
                    IMPORTS_CACHE[cache_key] = (
                        current / last / "__init__").with_suffix(ext)
                    return (current / last / "__init__").with_suffix(ext)
            else:
                for ext in PYTHON_EXTENSIONS:
                    if (current / last).with_suffix(ext).is_file():
                        IMPORTS_CACHE[cache_key] = (
                            current / last).with_suffix(ext)
                        return (current / last).with_suffix(ext)
                else:
                    for ext in PYTHON_EXTENSIONS:
                        if (current / "__init__").with_suffix(ext).is_file():
                            IMPORTS_CACHE[cache_key] = (
                                current / "__init__").with_suffix(ext)
                            return (current / last).with_suffix(ext)
        else:
            # some_module.some_submodule.some_variable
            # => Here some_module/some_submodule.py* might be a file
            for ext in PYTHON_EXTENSIONS:
                if (current.with_suffix(ext)).is_file():
                    IMPORTS_CACHE[cache_key] = current.with_suffix(ext)
                    return current.with_suffix(ext)
    else:
        raise ImportError(f"Couldn't find module '{full_name}'")


def get_imports(file: pathlib.Path,
                boundary: typing.Optional[pathlib.Path] = None,
                recursive: bool = True, no_fail: bool = True, safe: bool = True,
                parents: typing.Optional[typing.Set[pathlib.Path]] = None) -> typing.List[Import]:
    """
    Gets all imported files

    Parameters
    ----------
    file: pathlib.Path
        The file to get imports from
    boundary: Optional[pathlib.Path], default = None
        The boundary of the imports.
        This is used to bound the search to only a certain directory.
        If an import is made from outside the boundary, it is ignored.
    recursive: bool, default = True
        Whether to get imports recursively
    no_fail: bool, default = False
        Whether to raise an error if an import cannot be resolved
    safe: bool, default = True
        Whether to use the safe method of resolving imports
        or the unsafe method of resolving imports
    """
    parents = parents or set()
    if file in parents:
        raise ImportError("Circular import — "
                          "It is not possible to have the same import in a file later imported. "
                          f"(File: {file}))")

    parents.add(file)

    if boundary:
        boundary = pathlib.Path(boundary).resolve()

    imports: typing.List[Import] = []
    files: typing.Dict[pathlib.Path, Import] = {}

    file = pathlib.Path(file).resolve()

    with open(file, encoding="utf-8") as f:
        source = f.read()

    module = ast.parse(source)
    for element in ast.walk(module):
        if isinstance(element, ast.Import):
            # => import x,y,z
            # Import.names = [
            #     alias(name='x'),
            #     alias(name='y'),
            #     alias(name='z')]
            for name in element.names:
                location = ImportLocation(
                    file=file,
                    name=name.asname or name.name,
                    node=element
                )

                try:
                    resolved = resolve_import(
                        name.name, safe=safe, context=file.parent)
                except Exception:
                    if no_fail:
                        continue
                    raise

                if resolved in files:
                    for loc in files[resolved].locations:
                        if loc.node == element:
                            break
                    else:
                        files[resolved].locations.append(location)
                else:
                    res = Import(
                        file=resolved,
                        locations=[location]
                    )
                    files[resolved] = res
                    imports.append(res)

        if isinstance(element, ast.ImportFrom):
            # => from ..y import x,y,z
            # ImportFrom.module = 'y'
            # ImportFrom.names = [
            #     alias(name='x'),
            #     alias(name='y'),
            #     alias(name='z')]
            # ImportFrom.level = 2
            for name in element.names:
                location = ImportLocation(
                    file=file,
                    name=name.asname or name.name,
                    node=element
                )

                try:
                    resolved = resolve_import(name.name,
                                              module=element.module,
                                              level=element.level,
                                              safe=safe, context=file.parent)
                except Exception:
                    if no_fail:
                        continue
                    raise

                if resolved in files:
                    for loc in files[resolved].locations:
                        if loc.node == element:
                            break
                    else:
                        files[resolved].locations.append(location)
                else:
                    res = Import(
                        file=resolved,
                        locations=[location]
                    )
                    files[resolved] = res
                    imports.append(res)

    # Removing out of bound imports
    if boundary:
        imports = [imp for imp in imports if boundary in imp.file.parents]

    files = {imp.file: imp for imp in imports}

    if recursive:
        for imp in imports.copy():
            try:
                children = get_imports(imp.file,
                                       boundary=boundary,
                                       recursive=recursive,
                                       no_fail=no_fail, safe=safe,
                                       parents=parents)
            except Exception:
                if no_fail:
                    continue
                raise

            for child in children:
                if child.file in files:
                    for loc in child.locations:
                        # if loc.node in nodes:
                        if loc.file == file:
                            # Might be in a circular import
                            if no_fail:
                                continue
                            raise ImportError("Circular import — "
                                              "It is not possible to have the same import in a file later imported. "
                                              f"(File: {file})")
                        else:
                            files[child.file].locations.append(loc)
                else:
                    files[child.file] = child
                    imports.append(child)

    return imports


# if __name__ == "__main__":
#     c = Console()

#     with open("test.py", "r", encoding="utf-8") as f:
#         source = f.read()

#     c.print(info(source))

#     with open("test_clean.py", "w", encoding="utf-8") as f:
#         f.write(clean(source))
