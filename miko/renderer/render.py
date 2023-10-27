import ast
import pathlib
import typing
import os.path

from miko import static
from miko import parsers


def render_heading(message: str, level: int, base: int = 0):
    """Renders a heading of the given level"""
    return f"""\
{'#' * (level + base)} {message}
"""


def make_docs(source: str):
    # Recursively make docs for all modules in separate files
    pass


def make_module_docs(file: pathlib.Path):
    # Recursively make docs for all elements in the module
    pass


def make_class_docs(element: static.Element[ast.ClassDef], level: int = 0):
    # Recursively make docs for all elements in the class
    pass


def make_function_docs(element: static.Element[ast.FunctionDef | ast.AsyncFunctionDef], level: int = 0):
    pass

# Example


def render_example(example: str):
    """Renders an example code block"""
    # Single line example
    if "\n" not in example:
        return f"`{example}`\n"

    # Mutli line example
    return f"""\
```python
{example}
```
"""

# Accentuated Notes


def render_accentuated(level: str, message: str):
    """Renders a markdown accentuated note"""
    return f"""\
> **{level}**
> {message}
"""


def render_note(message: str):
    """Renders a markdown note"""
    return render_accentuated("Note", message)


def render_important(message: str):
    """Renders a markdown important note"""
    return render_accentuated("Important", message)


def render_warning(message: str):
    """Renders a markdown warning"""
    return render_accentuated("Warning", message)


def render_deprecated(element_type: str = "value"):
    """Renders a markdown deprecation warning"""
    return render_warning(f"This {element_type} is deprecated")


def render_source_link(source_file: pathlib.Path,
                       start: int, end: int, base_dir: typing.Optional[pathlib.Path] = None):
    """
    Renders a markdown source link

    Parameters
    ----------
    source_file: pathlib.Path
        The path to the source file
    start: int
        The start line number
    end: int
        The end line number
    base_dir: pathlib.Path, optional
        The base directory of the output directory to use for relative paths

    Returns
    -------
    str
        The markdown source link
    """
    try:
        base = pathlib.Path(base_dir or pathlib.Path() / "docs").absolute()
        source_file = pathlib.Path(source_file).absolute()
        common = pathlib.Path(os.path.commonpath([str(source_file),
                                                  str(base)])).resolve()
        # Getting the relative path
        path = pathlib.Path(source_file).resolve().relative_to(common)
        # Distance between the docs and the most deep common path
        # distance = str(base).count("/") - str(common).count("/") + 1
        distance = str(base).count("/") - str(common).count("/")
        path = pathlib.Path("../" * distance + str(path))
    except Exception:
        path = pathlib.Path(source_file)

    return f"> [Source: {path}]({path}#L{start}-L{end})\n"


def render_changelog(elements: parsers.changelog.Changelog):
    """Renders a markdown changelog"""
    def render_changelog_element(element: parsers.map.MapElement):
        return f"""<li><b>{element.name}</b>: {element.body}</li>"""

    rendered = "\n".join(render_changelog_element(element)
                         for element in elements)
    return f"""\
<details>
    <summary><b>Changelog</b></summary>
    <ul>
        {rendered}
    </ul>
</details>
"""


def render_copyright(elements: parsers.copyright.Copyright, level: int = 0):
    """Renders a markdown changelog"""
    def render_license(author: parsers.copyright.License):
        if author.year_from == author.year_to:
            result = f"""- **Copyright {author.name}**, *{author.year_from}*"""
        else:
            result = f"""- **Copyright {author.name}**"""
            result += f""", *{author.year_from} - {author.year_to}*"""

        if author.license:
            result += f""" ({author.license})"""

        if author.body:
            result += "\n" + author.body
        return result

    rendered = "\n".join(render_license(element)
                         for element in elements)

    return f"""\
{render_heading("Copyright", 2, level)}
{rendered}
"""


def render_description(description: str):
    return "  \n".join(description.splitlines()) + "\n"


def make_constant_docs(element: static.ConstantElement, source_file: pathlib.Path, parent_path: str = "", level: int = 0, base_dir: typing.Optional[pathlib.Path] = None):
    """Makes the documentation for a constant"""
    documentation = element.documentation

    results = []
    if parent_path:
        results.append(render_heading(f"{parent_path}.**{element.node.id}**",
                                      1, level))
    else:
        results.append(render_heading(f"**{element.node.id}**", 1, level))

    results.append(render_source_link(source_file, element.node.lineno, (element.node.end_lineno
                                                                         or element.node.lineno), base_dir))

    if documentation.description:
        results.append(render_description(documentation.description))

    if documentation.deprecated:
        results.append(render_deprecated())

    if documentation.examples:
        results.append(render_heading("Examples", 2, level))

        for index, example in enumerate(documentation.examples, start=1):
            results.append(render_heading(f"Example {index}", 3, level))
            results.append(render_example(example))

    for note in documentation.notes:
        results.append(render_note(note))

    for important in documentation.important:
        results.append(render_important(important))

    for warning in documentation.warnings:
        results.append(render_warning(warning))

    if documentation.changelog:
        results.append(render_changelog(documentation.changelog))

    if documentation.copyright:
        results.append(render_copyright(documentation.copyright))

    return "\n".join(results)
