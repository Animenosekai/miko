"""
This module contains the functions to render down the
documentationn elements to markdown
"""

import os.path
import pathlib
import typing

from miko import parsers
from miko.utils.empty import is_empty


def heading(message: str, level: int, base: int = 0):
    """Renders a heading of the given level"""
    return f"""\
{'#' * (level + base)} {message}
"""


def example(example: str):
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


def accentuated(level: str, message: str):
    """Renders a markdown accentuated note"""
    return f"""\
> **{level}**
> {message}
"""


def note(message: str):
    """Renders a markdown note"""
    return accentuated("Note", message)


def important(message: str):
    """Renders a markdown important note"""
    return accentuated("Important", message)


def warning(message: str):
    """Renders a markdown warning"""
    return accentuated("Warning", message)


def deprecated(element_type: str = "value"):
    """Renders a markdown deprecation warning"""
    return warning(f"This {element_type} is deprecated")


def source_link(source_file: pathlib.Path,
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

    if start == end:
        return f"> [Source: {path} @ line {start}]({path}#L{start})\n"
    return f"> [Source: {path} @ line {start}-{end}]({path}#L{start}-L{end})\n"


def changelog(elements: parsers.changelog.Changelog):
    """Renders a markdown changelog"""
    def changelog_element(element: parsers.map.MapElement):
        return f"""<li><b>{element.name}</b>: {element.body}</li>"""

    rendered = "\n".join(changelog_element(element)
                         for element in elements)
    return f"""\
<details>
    <summary><b>Changelog</b></summary>
    <ul>
        {rendered}
    </ul>
</details>
"""


def copyright(elements: parsers.copyright.Copyright):
    """Renders a markdown copyright"""
    def license(author: parsers.copyright.License):
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

    rendered = "\n".join(license(element)
                         for element in elements)

    return rendered


def stringify_type(t: typing.Any):
    """Stringifies a type"""
    if hasattr(t, "__name__"):
        return t.__name__
    return str(t)


def parameters(paremeters: parsers.parameters.Parameters):
    """Renders a markdown parameters"""
    def render_parameter(parameter: parsers.parameters.Parameter):
        additions = []
        if parameter.deprecated:
            additions.append("Note: This parameter is **deprecated**")
        if parameter.default and not is_empty(parameter.default):
            additions.append(f"Default Value: `{parameter.default}`")
        elif parameter.optional:
            additions.append("This value is **optional**")
        if parameter.body:
            additions.append(parameter.body)
        rendered_body = ""
        for element in additions:
            rendered_body += f"  - {element}\n"
        if parameter.types:
            rendered_types = f""": {', '.join(stringify_type(t)
                                              for t in parameter.types)}"""
        else:
            rendered_types = ""
        return f"""\
- **{parameter.name}**{rendered_types}
{rendered_body}
"""
    return "\n".join(render_parameter(parameter) for parameter in paremeters)


def returns(returns: parsers.returns.Returns):
    """Renders a markdown returns"""
    def render_return(value: parsers.map.MapElement):
        if not value.body:
            return f"""- {stringify_type(value.name)}\n"""
        return f"""\
- {stringify_type(value.name)}
    - {value.body}
"""
    return "\n".join(render_return(val) for val in returns)


def yields(yields: parsers.yields.Yields):
    """Renders a markdown returns"""
    def render_yield(value: parsers.map.MapElement):
        if not value.body:
            return f"""- {stringify_type(value.name)}\n"""
        return f"""\
- {stringify_type(value.name)}
    - {value.body}
"""
    return "\n".join(render_yield(val) for val in yields)


def raises(raises: parsers.raises.Raises):
    """Renders a markdown raises"""
    def render_raise(value: parsers.map.MapElement):
        if not value.body:
            return f"""- {stringify_type(value.name)}\n"""
        return f"""\
- {stringify_type(value.name)}
    - {value.body}
"""
    return "\n".join(render_raise(val) for val in raises)


def description(description: str):
    """Renders a markdown description"""
    return "  \n".join(description.splitlines()) + "\n"
