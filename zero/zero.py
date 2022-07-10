import inspect
import parser.example
import parser.list
import types
import typing


class Function:
    def __init__(self, func: typing.Callable) -> None:
        self.original = func
        self.name = self.original.__name__
        self.signature = inspect.signature(func)
        self.docs = Docs(self.original.__doc__ if self.original.__doc__ is not None else "No description", self.signature)
        self.code = Function.get_code(self.original)
        self.source_filename = self.code.co_filename
        self.source_linenumber = self.code.co_firstlineno
        self.source_name = self.code.co_name
        self.local_variables = self.code.co_names
        self.parameters = self.signature.parameters
        self.return_annotation = self.signature.return_annotation

    @staticmethod
    def get_code(obj: typing.Any) -> types.CodeType:
        """
        Returns the __code__ object of a given callable object.

        Parameters
        ----------
        obj: Callable
            The object to get the __code__ from

        Returns
        -------
        CodeType
            The __code__ object
        """
        if inspect.ismethod(obj):
            obj = obj.__func__
        if inspect.isfunction(obj):
            obj = obj.__code__
        if inspect.istraceback(obj):
            obj = obj.tb_frame
        if inspect.isframe(obj):
            obj = obj.f_code
        if not inspect.iscode(obj):
            raise TypeError('method, function, traceback, frame, or code object was expected, got {}'.format(type(obj).__name__))
        return obj

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

    "EXAMPLES": parser.example.Example,
    "EXAMPLE": parser.example.Example
}


class Docs:
    parameters: parser.list.Parameters
    returns: parser.list.Returns
    raises: parser.list.Raises
    changelog: parser.list.Changelog
    copyright: parser.list.Copyright
    example: parser.example.Example
    warnings: typing.List[str]
    notes: typing.List[str]

    def __init__(self, docs: str, signature: inspect.Signature = None) -> None:
        self.original = inspect.cleandoc(str(docs))
        self.elements = {}

        self.warnings = []
        self.notes = []

        missing = {
            parser.list.Parameters.__map_attribute__: parser.list.Parameters,
            parser.list.Returns.__map_attribute__: parser.list.Returns,
            parser.list.Raises.__map_attribute__: parser.list.Raises,
            parser.list.Changelog.__map_attribute__: parser.list.Changelog,
            parser.list.Copyright.__map_attribute__: parser.list.Copyright,
            parser.example.Example.__map_attribute__: parser.example.Example
        }

        self.description = []

        for section in self.original.split("\n\n"):
            name, _, body = section.partition("\n---")
            if not body:
                self.description.append(name)  # name would be the content here
                continue
            parse = SECTIONS_MAP.get(name.replace(" ", "").upper().strip(), None)
            if parse is None:
                self.description.append("\n---".join((name, body)))
                continue
            content = body.lstrip("-").lstrip("\n")
            try:
                self.elements[parse.__map_attribute__].extend(content)
            except Exception:
                self.elements[parse.__map_attribute__] = parse(content, signature=signature)
                missing.pop(parse.__map_attribute__, None)

        if signature:
            if parser.list.Parameters.__map_attribute__ not in self.elements:
                self.elements[parser.list.Parameters.__map_attribute__] = parser.list.Parameters(signature=signature)
                missing.pop(parser.list.Parameters.__map_attribute__, None)

            if parser.list.Returns.__map_attribute__ not in self.elements:
                self.elements[parser.list.Returns.__map_attribute__] = parser.list.Returns(signature=signature)
                missing.pop(parser.list.Returns.__map_attribute__, None)

        for attr, parse in missing.items():
            self.elements[attr] = parse()

        # HANDLING TAGS
        for index, line in enumerate(self.description):
            start, _, content = str(line).partition(":")
            start = start.replace(" ", "").upper().strip()
            content = content.strip()
            if start in {"WARNING", "WARNINGS"}:
                self.warnings.append(content)
                self.description[index] = "Warning: {content}".format(content=content)
            elif start in {"NOTE", "NOTES", "SEEALSO", "INFORMATION"}:
                self.notes.append(content)
                self.description[index] = "Note: {content}".format(content=content)

        if len(self.description) > 0:
            self.deprecated = str(self.description[0]).replace(" ", "").upper().startswith("!DEPRECATED!")
            if self.deprecated:
                index = self.description[0].find("!")
                second_index = index + self.description[0][index + 1:].find("!") + 2
                self.description[0] = "! DEPRECATED !" + self.description[0][second_index:]

    def __repr__(self) -> str:
        return "<Docs sections={sections}>".format(sections=list(self.elements.keys()))

    def __getattr__(self, key: str):
        return self.elements.__getitem__(key)

    def dumps(self, indent=4):
        result = ""
        result += "\n\n".join(self.description)
        result += "\n\n"
        sections = []
        for section in (self.parameters, self.returns, self.raises, self.example, self.changelog, self.copyright):
            if not isinstance(section, parser.example.Example) and len(section) <= 0:
                continue

            current_section = ""

            current_section += section.__class__.__name__ + "\n"
            current_section += "-" * len(section.__class__.__name__) + "\n"

            if isinstance(section, parser.example.Example):
                current_section += section.original + "\n"
            else:
                for element in section:
                    # element = self.parameters.__element_type__()
                    current_section += element.name

                    if isinstance(element, parser.list.Parameter):
                        options = []
                        if len(element.types) > 0:
                            options.append(" | ".join([v.__name__ if isinstance(v, type) else str(v) for v in element.types]))
                        if element.default:
                            options.append("default = {default}".format(default=element.default))
                        elif element.optional:
                            options.append("optional")
                        if element.deprecated:
                            options.append("deprecated")

                        if len(options) > 0:
                            current_section += ": " + ", ".join(options)

                    current_section += "\n"

                    for sentence in element.content:
                        current_section += " " * indent + sentence + "\n"

            sections.append(current_section)

        result += "\n\n".join(sections)

        return result


a = Function(func)
b = Function(func_without_docs)
c = Function(func_bad)
