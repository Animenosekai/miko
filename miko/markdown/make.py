"""
This module contains functions for making documentation from the AST.
"""
import ast
import pathlib
import typing

from miko import static
from miko.markdown import render, tree


def PrivateElement(element: static.Element):
    """Returns True if the given element is private"""
    return element.is_private


def make_docs(entry_point: pathlib.Path,
              output_dir: pathlib.Path,
              file_filter: typing.Callable[[pathlib.Path],
                                           bool] = lambda x: False,
              element_filter: typing.Callable[[static.Element], bool] = PrivateElement):
    """
    Makes the documentation for the every file loaded by the entry point

    Note: An entry point could be for example the __init__.py file of a library
    """
    entry_point = pathlib.Path(entry_point).resolve()
    output_dir = pathlib.Path(output_dir).resolve()
    imports = static.get_imports(entry_point, entry_point.parent)

    make_module_docs(entry_point, output_dir / entry_point.with_suffix(".md"))

    for imp in imports:
        if file_filter(imp.file):
            continue
        if imp.file.stem == "__init__":
            output_file = output_dir / \
                imp.file.relative_to(entry_point.parent).with_name("README.md")
        else:
            output_file = output_dir / \
                imp.file.relative_to(entry_point.parent).with_suffix(".md")
        make_module_docs(imp.file, output_file, element_filter=element_filter)


def make_module_docs(source_file: pathlib.Path, output_file: pathlib.Path, element_filter: typing.Callable[[static.Element], bool] = PrivateElement):
    """Makes the documentation for a module"""
    source_file = pathlib.Path(source_file).resolve()
    output_file = pathlib.Path(output_file).resolve()
    with open(source_file) as f:
        r = ast.parse(f.read())
    elements = static.get_elements(r)
    for element in elements:
        if isinstance(element.node, ast.Module):
            output_file.parent.mkdir(parents=True, exist_ok=True)
            rendered = render_module_docs(element, elements, source_file,
                                          base_dir=output_file.parent)
            return output_file.write_text(rendered)


def render_module_docs(element: static.ConstantElement,
                       elements: typing.List[static.Element],
                       source_file: pathlib.Path,
                       level: int = 0,
                       parent_path: str = "",
                       base_dir: typing.Optional[pathlib.Path] = None,
                       element_filter: typing.Callable[[static.Element], bool] = PrivateElement):
    """Makes the documentation for a module"""
    documentation = element.documentation

    results = []
    if parent_path:
        results.append(render.heading(f"*module* {parent_path}.**{source_file.stem}**",
                                      1, level))
        # parent_path = f"{parent_path}.{source_file.stem}"
    else:
        results.append(render.heading(f"*module* **{source_file.stem}**",
                                      1, level))
        # parent_path = source_file.stem

    results.append(render.source_link(source_file, 0, 0, base_dir))

    if documentation.description:
        results.append(render.description(documentation.description))

    if documentation.deprecated:
        results.append(render.deprecated())

    for note in documentation.notes:
        results.append(render.note(note))

    for important in documentation.important:
        results.append(render.important(important))

    for warning in documentation.warnings:
        results.append(render.warning(warning))

    if documentation.examples:
        results.append(render.heading("Examples", 2, level))

        for index, example in enumerate(documentation.examples, start=1):
            results.append(render.heading(f"Example {index}", 3, level))
            results.append(render.example(example))

    if documentation.copyright:
        results.append(render.heading("Copyright", 2, level))
        results.append(render.copyright(documentation.copyright))

    if documentation.changelog:
        results.append(render.changelog(documentation.changelog))

    for child in tree.get_direct_children(element, elements=elements):
        if element_filter(child):
            continue

        if isinstance(child.node, ast.Name):
            results.append(render_constant_docs(child, source_file, level + 1,
                                                parent_path=parent_path, base_dir=base_dir))
        elif isinstance(child.node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results.append(render_function_docs(child, source_file, level + 1,
                                                parent_path=parent_path, base_dir=base_dir))
        elif isinstance(child.node, ast.ClassDef):
            results.append(render_class_docs(child, elements, source_file, level + 1,
                                             parent_path=parent_path, base_dir=base_dir, element_filter=element_filter))
    return "\n".join(results)


def render_class_docs(element: static.Element[ast.ClassDef],
                      elements: typing.List[static.Element],
                      source_file: pathlib.Path,
                      level: int = 0,
                      parent_path: str = "",
                      base_dir: typing.Optional[pathlib.Path] = None,
                      element_filter: typing.Callable[[static.Element], bool] = PrivateElement):
    # Recursively make docs for all elements in the class
    documentation = element.documentation

    results = []

    if parent_path:
        results.append(render.heading(f"*class* {parent_path}.**{element.node.name}**",
                                      1, level))
        parent_path = f"{parent_path}.{element.node.name}"
    else:
        results.append(render.heading(f"*class* **{element.node.name}**",
                                      1, level))
        parent_path = element.node.name

    results.append(render.source_link(source_file, element.node.lineno, (element.node.end_lineno
                                                                         or element.node.lineno), base_dir))

    if documentation.description:
        results.append(render.description(documentation.description))

    if documentation.deprecated:
        results.append(render.deprecated())

    if documentation.parameters:
        results.append(render.heading("Parameters", 2, level))
        results.append(render.parameters(documentation.parameters))

    if documentation.returns:
        results.append(render.heading("Returns", 2, level))
        results.append(render.returns(documentation.returns))

    if documentation.yields:
        results.append(render.heading("Yields", 2, level))
        results.append(render.yields(documentation.yields))

    if documentation.raises:
        results.append(render.heading("Raises", 2, level))
        results.append(render.raises(documentation.raises))

    for note in documentation.notes:
        results.append(render.note(note))

    for important in documentation.important:
        results.append(render.important(important))

    for warning in documentation.warnings:
        results.append(render.warning(warning))

    if documentation.examples:
        results.append(render.heading("Examples", 2, level))

        for index, example in enumerate(documentation.examples, start=1):
            results.append(render.heading(f"Example {index}", 3, level))
            results.append(render.example(example))

    if documentation.copyright:
        results.append(render.heading("Copyright", 2, level))
        results.append(render.copyright(documentation.copyright))

    if documentation.changelog:
        results.append(render.changelog(documentation.changelog))

    for child in tree.get_direct_children(element, elements=elements):
        if element_filter(child):
            continue

        if isinstance(child.node, ast.Name):
            results.append(render_constant_docs(child, source_file, level + 1,
                                                parent_path=parent_path, base_dir=base_dir))
        elif isinstance(child.node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results.append(render_function_docs(child, source_file, level + 1,
                                                parent_path=parent_path, base_dir=base_dir))
        elif isinstance(child.node, ast.ClassDef):
            results.append(render_class_docs(child, elements, source_file, level + 1,
                                             parent_path=parent_path, base_dir=base_dir, element_filter=element_filter))

    return "\n".join(results)


def render_constant_docs(element: static.ConstantElement,
                         source_file: pathlib.Path,
                         level: int = 0,
                         parent_path: str = "",
                         base_dir: typing.Optional[pathlib.Path] = None):
    """Makes the documentation for a constant"""
    documentation = element.documentation

    results = []
    if parent_path:
        results.append(render.heading(f"*const* {parent_path}.**{element.node.id}**",
                                      1, level))
    else:
        results.append(render.heading(
            f"*const* **{element.node.id}**", 1, level))

    results.append(render.source_link(source_file, element.node.lineno, (element.node.end_lineno
                                                                         or element.node.lineno), base_dir))

    if documentation.description:
        results.append(render.description(documentation.description))

    if documentation.deprecated:
        results.append(render.deprecated())

    for note in documentation.notes:
        results.append(render.note(note))

    for important in documentation.important:
        results.append(render.important(important))

    for warning in documentation.warnings:
        results.append(render.warning(warning))

    if documentation.examples:
        results.append(render.heading("Examples", 2, level))

        for index, example in enumerate(documentation.examples, start=1):
            results.append(render.heading(f"Example {index}", 3, level))
            results.append(render.example(example))

    if documentation.copyright:
        results.append(render.heading("Copyright", 2, level))
        results.append(render.copyright(documentation.copyright))

    if documentation.changelog:
        results.append(render.changelog(documentation.changelog))

    return "\n".join(results)


def render_function_docs(element: static.Element[ast.FunctionDef | ast.AsyncFunctionDef],
                         source_file: pathlib.Path,
                         level: int = 0,
                         parent_path: str = "",
                         base_dir: typing.Optional[pathlib.Path] = None):
    """Makes the documentation for a function"""
    documentation = element.documentation

    results = []

    if isinstance(element.node, ast.AsyncFunctionDef):
        func_type = "async func"
    else:
        func_type = "func"

    if parent_path:
        results.append(render.heading(f"*{func_type}* {parent_path}.**{element.node.name}**",
                                      1, level))
    else:
        results.append(render.heading(f"*{func_type}* **{element.node.name}**",
                                      1, level))

    results.append(render.source_link(source_file, element.node.lineno, (element.node.end_lineno
                                                                         or element.node.lineno), base_dir))

    if documentation.description:
        results.append(render.description(documentation.description))

    if documentation.deprecated:
        results.append(render.deprecated())

    if documentation.parameters:
        results.append(render.heading("Parameters", 2, level))
        results.append(render.parameters(documentation.parameters))

    if documentation.returns:
        results.append(render.heading("Returns", 2, level))
        results.append(render.returns(documentation.returns))

    if documentation.yields:
        results.append(render.heading("Yields", 2, level))
        results.append(render.yields(documentation.yields))

    if documentation.raises:
        results.append(render.heading("Raises", 2, level))
        results.append(render.raises(documentation.raises))

    for note in documentation.notes:
        results.append(render.note(note))

    for important in documentation.important:
        results.append(render.important(important))

    for warning in documentation.warnings:
        results.append(render.warning(warning))

    if documentation.examples:
        results.append(render.heading("Examples", 2, level))

        for index, example in enumerate(documentation.examples, start=1):
            results.append(render.heading(f"Example {index}", 3, level))
            results.append(render.example(example))

    if documentation.copyright:
        results.append(render.heading("Copyright", 2, level))
        results.append(render.copyright(documentation.copyright))

    if documentation.changelog:
        results.append(render.changelog(documentation.changelog))

    return "\n".join(results)
