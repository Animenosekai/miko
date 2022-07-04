from test import func
import typing
import inspect
import parser.list
import parser.tag


class Function:
    def __init__(self, func: typing.Callable) -> None:
        self.signature = inspect.signature(func)


SECTIONS_MAP = {
    "PARAMETERS": parser.list.Parameters,
    "PARAMETER": parser.list.Parameters,
    "PARAMS": parser.list.Parameters,
    "PARAM": parser.list.Parameters,

    "RETURNS": parser.list.Returns,
    "RETURN": parser.list.Returns,
    "RETURNING": parser.list.Returns,

    "RAISES": parser.list.Raises,
    "RAISE": parser.list.Raises,
    "EXCEPTIONS": parser.list.Raises,
    "EXCEPTION": parser.list.Raises,
    "ERRORS": parser.list.Raises,
    "ERROR": parser.list.Raises,

    "CHANGELOG": parser.list.Changelog,
    "CHANGES": parser.list.Changelog,

    "COPYRIGHTS": parser.list.Copyright,
    "COPYRIGHT": parser.list.Copyright,
    "AUTHORS": parser.list.Copyright,
    "AUTHOR": parser.list.Copyright,

    "WARNINGS": parser.tag.Warning,
    "WARNING": parser.tag.Warning,

    "NOTES": parser.tag.Note,
    "NOTE": parser.tag.Note,
    "SEEALSO": parser.tag.Note,
    "INFORMATION": parser.tag.Note
}


class Docs:
    def __init__(self, docs: str, signature: inspect.Signature = None) -> None:
        self.original = inspect.cleandoc(str(docs))
        self.elements = {}
        description = []
        for section in self.original.split("\n\n"):
            name, _, body = section.partition("\n---")
            if not body:
                description.append(name)  # name would be the content here
                continue
            name = name.replace(" ", "").upper()
            parse = SECTIONS_MAP.get(name, None)
            if parse is None:
                description.append("\n---".join((name, body)))
                continue
            content = parse(body.lstrip("-").lstrip("\n"))
            try:
                self.elements[parse.__name__].append(content)
            except Exception:
                self.elements[parse.__name__] = [content]

Docs(func.__doc__)
