"""
miko.py

Contains the main code for the Miko documentation style
"""

import inspect
import types
import typing

from miko import parsers


class Function:
    """Retrieves information on a given function"""

    def __init__(self, func: typing.Callable) -> None:
        self.original = func
        self.name = self.original.__name__
        self.signature = inspect.signature(func)
        self.docs = Documentation(
            docstring=self.original.__doc__ if self.original.__doc__ is not None else "No description",
            signature=self.signature
        )
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
            raise TypeError(f'''method, function, traceback, frame,\
                or code object was expected, got {type(obj).__name__}''')
        return obj

    def __repr__(self) -> str:
        return "<Function '{name}'>".format(name=self.name)


class Documentation:
    """Parses a docstring"""
    original: str
    """Original text"""
    description: str
    """The description"""

    # Flags
    deprecated: parsers.deprecated.Deprecated

    # Inline Parsers
    notes: parsers.notes.Notes
    """Notes about the element"""
    warnings: parsers.warnings.Warnings
    """Warnings about the element"""
    important: parsers.important.Important
    """Important notes about the element"""

    example: parsers.example.Example
    """Examples of usage"""

    # Map Parsers
    parameters: parsers.parameters.Parameters
    """Parameters for the callable"""
    returns: parsers.returns.Returns
    """Return value for the callable"""
    yields: parsers.yields.Yields
    """Return value for the callable"""
    raises: parsers.raises.Raises
    """Raisable exception by the callable"""
    changelog: parsers.changelog.Changelog
    """Changelog of the element"""
    copyright: parsers.copyright.Copyright
    """Copyright notes for the element"""

    def __init__(self,
                 docstring: str,
                 flag_prefix: str = "!",
                 **kwargs) -> None:
        self.__annotations__ = (self.__annotations__
                                if hasattr(self, "__annotations__")
                                else {})
        """The different type annotations for the class"""

        self.extra_arguments = kwargs
        """The extra arguments passed with the docstring parser"""

        self.flag_prefix = str(flag_prefix)

        block_map: typing.Dict[str, str] = {}
        inline_map: typing.Dict[str, str] = {}
        flag_map: typing.Dict[str, str] = {}

        for attr, annotation in self.__annotations__.items():
            for mapping, parser in [(block_map, parsers.map.MapParser),
                                    (inline_map, parsers.inline.InlineParser),
                                    (flag_map, parsers.flag.FlagParser)]:
                if issubclass(annotation, parser):
                    for name in annotation.names:
                        name = self._normalize_name(name)
                        mapping[name] = attr
                    setattr(self, attr, annotation(**self.extra_arguments))

        self.original = inspect.cleandoc(str(docstring or ""))

        description = []

        # Handling the different sections
        # Example:

        # Section 1
        # ---------
        # Do something
        #
        # Section 2
        # ---------
        # Do another thing

        # Between "Do something" and "Section 2", there are two newline characters
        for section in self.original.split("\n\n"):
            # Between "Section 1" and the content,
            # there is a newline character and at least 3 hyphens
            name, _, body = section.partition("\n---")

            # Nothing describing the paragraph
            # Example:
            #
            # Section 1
            # ---------
            # (no content)
            if not body:
                # The section should be considered as a description element
                description.append(name)  # name would be the content here
                continue

            # Getting the parser
            name = self._normalize_name(name)
            attr = block_map.get(name, None)
            if attr is None:
                attr = inline_map.get(name, None)

            # If there is no parser associated with the paragraph name
            if attr is None:
                # Reconstruct the content and add it to the description body
                description.append("\n---".join((name, body)))
                continue

            # Removing the extra hyphens and the newline character
            content = body.lstrip("-").lstrip("\n")

            # Block parser
            current = getattr(self, attr)
            if isinstance(current, parsers.map.MapParser):
                current.extend(content)
            if isinstance(current, parsers.inline.InlineParser):
                current.append(content)

            # Not added to the description because parsed blocks
            # are not description content

        for line in description.copy():
            line = str(line).strip()

            if line.startswith(self.flag_prefix):
                flag = line.removeprefix(self.flag_prefix)
                flag = self._normalize_name(flag)

                flag_attr = flag_map.get(flag, None)

                if flag_attr:
                    getattr(self, flag_attr).set_flag()
                    description.remove(line)
                    continue

            start, _, content = str(line).partition(":")

            start = self._normalize_name(start)
            content = content.strip()

            if not content:
                continue

            # Inline parser
            attr = inline_map.get(start, None)
            if attr is None:
                continue

            getattr(self, attr).append(content)

            # Not part of the description anymore
            description.remove(line)

        self.description = "\n".join(description)

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Cleans the name to normalize it"""
        return name.replace(" ", "").upper().strip()

    def dumps(self, indent: int = 4):
        """Returns a clean docstring"""
        result = ""

        # Adding back the description if it has content
        if self.description.replace(" ", ""):
            result += self.description
            result += "\n\n"

        # Adding flags
        for attr in self.__annotations__:
            parser = getattr(self, attr)
            if isinstance(parser, parsers.flag.FlagParser):
                element = parser.dumps(indent=indent)
                if element:
                    result += element
                    result += "\n\n"

        # Adding inline sections
        for attr in self.__annotations__:
            parser = getattr(self, attr)
            if isinstance(parser, parsers.inline.InlineParser):
                element = parser.dumps(indent=indent)
                if element:
                    result += element
                    result += "\n\n"

        # Adding block sections
        for attr in self.__annotations__:
            parser = getattr(self, attr)
            if isinstance(parser, parsers.map.MapParser):
                element = parser.dumps(indent=indent)
                if element:
                    result += element
                    result += "\n\n"

        return result.strip().strip("\n")

    def __repr__(self) -> str:
        representations = [f"{attr}={getattr(self, attr)}"
                           for attr, annotation in self.__annotations__.items()
                           if getattr(self, attr) and issubclass(annotation, (parsers.parser.Parser, parsers.flag.FlagParser))]
        return f"{self.__class__.__name__}({', '.join(representations)})"


# Backward compatibility
Docs = Documentation
