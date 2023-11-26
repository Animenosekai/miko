"""
This module contains the functions to render down the
documentationn elements to markdown
"""
import os.path
import pathlib
import typing

from miko import parsers, static
from miko.utils.empty import is_empty


def heading(message: str, level: int, base: int = 0):
    """
    Renders a heading of the given level

    Parameters
    ----------
    message: str
    level: int
    base: int, default = 0
    """
    return f"{'#' * (level + base)} {message}\n"


def example(example: str):
    """
    Renders an example code block

    Parameters
    ----------
    example: str
    """
    # Single line example
    if "\n" not in example:
        return f"`{example}`\n"
    # Mutli line example
    return f"```python\n{example}\n```\n"


def accentuated(level: str, message: str):
    """
    Renders a markdown accentuated note

    Parameters
    ----------
    level: str
    message: str
    """
    return f"> [!{level}]\n> {message}\n"


def note(message: str):
    """
    Renders a markdown note

    Parameters
    ----------
    message: str
    """
    return accentuated("NOTE", message)


def important(message: str):
    """
    Renders a markdown important note

    Parameters
    ----------
    message: str
    """
    return accentuated("IMPORTANT", message)


def warning(message: str):
    """
    Renders a markdown warning

    Parameters
    ----------
    message: str
    """
    return accentuated("WARNING", message)


def tip(message: str):
    """
    Renders a markdown tip

    Parameters
    ----------
    message: str
    """
    return accentuated("TIP", message)


def caution(message: str):
    """
    Renders a markdown caution

    Parameters
    ----------
    message: str
    """
    return accentuated("CAUTION", message)


def deprecated(element_type: str = "value"):
    """
    Renders a markdown deprecation warning

    Parameters
    ----------
    element_type: str, default = value
    """
    return warning(f"This {element_type} is deprecated")


def relative_link(
    source_file: pathlib.Path, base_dir: typing.Optional[pathlib.Path] = None
):
    """
    Parameters
    ----------
    source_file: Path
    base_dir: NoneType | Path, default = None
    """
    try:
        base = pathlib.Path(base_dir or pathlib.Path() / "docs").absolute()
        source_file = pathlib.Path(source_file).absolute()
        common = pathlib.Path(
            os.path.commonpath([str(source_file), str(base)])
        ).resolve()
        # Getting the relative path
        path = pathlib.Path(source_file).resolve().relative_to(common)
        # Distance between the docs and the most deep common path
        # distance = str(base).count("/") - str(common).count("/") + 1
        distance = str(base).count("/") - str(common).count("/")
        path = pathlib.Path("../" * distance + str(path))
    except Exception:
        path = pathlib.Path(source_file)
    return path


def source_link(
    source_file: pathlib.Path,
    start: int,
    end: int,
    base_dir: typing.Optional[pathlib.Path] = None,
):
    """
    Renders a markdown source link

    Parameters
    ----------
    source_file: Path
        The path to the source file
    start: int
        The start line number
    end: int
        The end line number
    base_dir: NoneType | Path, default = None
        The base directory of the output directory to use for relative paths

    Returns
    -------
    str
        The markdown source link
    """
    path = relative_link(source_file, base_dir)
    if start == end:
        return f"> [Source: {path} @ line {start}]({path}#L{start})\n"
    return f"> [Source: {path} @ line {start}-{end}]({path}#L{start}-L{end})\n"


def imports(
    imports: typing.List[static.Import], base_dir: typing.Optional[pathlib.Path] = None
):
    """
    Renders a markdown imports

    Parameters
    ----------
    imports: list
    base_dir: NoneType | Path, default = None
    """

    def render_import(value: static.Import):
        """
        Parameters
        ----------
        value: static.Import
        """
        path = relative_link(value.file, base_dir)
        locations = ", ".join((f"`{loc.name}`" for loc in value.locations))
        return f"- [{path}]({path}): As {locations}\n"

    return "\n".join((render_import(val) for val in imports))


def changelog(elements: parsers.changelog.Changelog):
    """
    Renders a markdown changelog

    Parameters
    ----------
    elements: parsers.changelog.Changelog
    """

    def changelog_element(element: parsers.map.MapElement):
        """
        Parameters
        ----------
        element: parsers.map.MapElement
        """
        return f"<li><b>{element.name}</b>: {element.body}</li>"

    rendered = "\n".join((changelog_element(element) for element in elements))
    return f"<details>\n    <summary><b>Changelog</b></summary>\n    <ul>\n        {rendered}\n    </ul>\n</details>\n"


def copyright(elements: parsers.copyright.Copyright):
    """
    Renders a markdown copyright

    Parameters
    ----------
    elements: parsers.copyright.Copyright
    """

    def license(author: parsers.copyright.License):
        """
        Parameters
        ----------
        author: parsers.copyright.License
        """
        result = f"- **{author.name}**"
        if author.year_from:
            if author.year_from == author.year_to or not author.year_to:
                result += f", *{author.year_from}*"
            else:
                result += f", *{author.year_from} - {author.year_to}*"
        if author.license:
            result += f" ({author.license})"
        if author.body:
            result += "\n" + author.body
        return result

    rendered = "\n".join((license(element) for element in elements))
    return rendered


def stringify_type(t: typing.Any):
    """
    Stringifies a type

    Parameters
    ----------
    t: Any
    """
    if hasattr(t, "__name__"):
        return f"`{t.__name__}`"
    return f"`{t}`"


def parameters(parameters: parsers.parameters.Parameters):
    """
    Renders a markdown parameters

    Parameters
    ----------
    parameters: parsers.parameters.Parameters
    """

    def render_parameter(parameter: parsers.parameters.Parameter):
        """
        Parameters
        ----------
        parameter: parsers.parameters.Parameter
        """
        additions = []
        if parameter.deprecated:
            additions.append("Note: This parameter is **deprecated**")
        if parameter.default and (not is_empty(parameter.default)):
            additions.append(f"Default Value: `{parameter.default}`")
        elif parameter.optional:
            additions.append("This value is **optional**")
        if parameter.body:
            additions.append(parameter.body)
        rendered_body = ""
        for element in additions:
            rendered_body += f"  - {element}\n"
        if parameter.types:
            rendered_types = f": {', '.join(sorted(set((stringify_type(t) for t in parameter.types))))}"
        else:
            rendered_types = ""
        return f"- **{parameter.name}**{rendered_types}\n{rendered_body}\n"

    return "\n".join(
        (
            render_parameter(parameter)
            for parameter in sorted(parameters, key=lambda x: x.name)
        )
    )


def returns(returns: parsers.returns.Returns):
    """
    Renders a markdown returns

    Parameters
    ----------
    returns: parsers.returns.Returns
    """

    def render_return(value: parsers.map.MapElement):
        """
        Parameters
        ----------
        value: parsers.map.MapElement
        """
        if not value.body:
            return f"- {stringify_type(value.name)}\n"
        return f"- {stringify_type(value.name)}\n    - {value.body}\n"

    return "\n".join(
        (render_return(val) for val in sorted(returns, key=lambda x: x.name))
    )


def yields(yields: parsers.yields.Yields):
    """
    Renders a markdown returns

    Parameters
    ----------
    yields: parsers.yields.Yields
    """

    def render_yield(value: parsers.map.MapElement):
        """
        Parameters
        ----------
        value: parsers.map.MapElement
        """
        if not value.body:
            return f"- {stringify_type(value.name)}\n"
        return f"- {stringify_type(value.name)}\n    - {value.body}\n"

    return "\n".join(
        (render_yield(val) for val in sorted(yields, key=lambda x: x.name))
    )


def raises(raises: parsers.raises.Raises):
    """
    Renders a markdown raises

    Parameters
    ----------
    raises: parsers.raises.Raises
    """

    def render_raise(value: parsers.map.MapElement):
        """
        Parameters
        ----------
        value: parsers.map.MapElement
        """
        if not value.body:
            return f"- {stringify_type(value.name)}\n"
        return f"- {stringify_type(value.name)}\n    - {value.body}\n"

    return "\n".join(
        (render_raise(val) for val in sorted(raises, key=lambda x: x.name))
    )


def description(description: str):
    """
    Renders a markdown description

    Parameters
    ----------
    description: str
    """
    return "  \n".join(description.splitlines()) + "\n"

