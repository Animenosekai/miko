from test import func, func_without_docs
import typing
import inspect
import parser.list
import parser.tag


class Function:
    def __init__(self, func: typing.Callable) -> None:
        self.original = func
        self.name = self.original.__name__
        self.signature = inspect.signature(func)
        self.docs = Docs(self.original.__doc__, self.signature)

    def __repr__(self) -> str:
        return "<Function '{name}'>".format(name=self.name)


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
    parameters: parser.list.Parameters
    returns: parser.list.Returns
    raises: parser.list.Raises
    changelog: parser.list.Changelog
    copyright: parser.list.Copyright

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
            content = body.lstrip("-").lstrip("\n")
            try:
                self.elements[parse.__map_attribute__].extend(content)
            except Exception:
                self.elements[parse.__map_attribute__] = parse(content, signature=signature)

        if signature:
            if parser.list.Parameters.__map_attribute__ not in self.elements:
                self.elements[parser.list.Parameters.__map_attribute__] = parser.list.Parameters(signature=signature)

            if parser.list.Returns.__map_attribute__ not in self.elements:
                self.elements[parser.list.Returns.__map_attribute__] = parser.list.Returns(signature=signature)

    def __repr__(self) -> str:
        return "<Docs sections={sections}>".format(sections=list(self.elements.keys()))

    def __getattr__(self, key: str):
        return self.elements.__getitem__(key)


a = Function(func)
b = Function(func_without_docs)
