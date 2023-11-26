"""
miko.py
Contains the main code for the Miko documentation style
"""
import dataclasses
import inspect
import types
import typing

from miko import parsers


class Callable:
    """
    Retrieves information on a given function

    Raises
    ------
    TypeError
    """

    @dataclasses.dataclass
    class Source:
        """Stores information on the source of a callable"""

        filename: str
        "The filename where the callable was defined"
        line: int
        "The line where the callable was defined"
        name: str
        "The original name of the callable"

    def __init__(self, func: typing.Callable) -> None:
        """
        Parameters
        ----------
        func: () -> Any
        """
        self.callable = func
        "The callable object"
        self.name = self.callable.__name__
        "The name of the callable"
        self.signature = inspect.signature(func)
        "The signature of the callable"
        self.docs = Documentation(
            docstring=self.callable.__doc__ if self.callable.__doc__ else "",
            signature=self.signature,
            noself=inspect.ismethod(self.callable),
        )
        "The documentation of the callable"
        self.code = Callable.get_code(self.callable)
        "The code object of the callable"
        self.source = self.Source(
            filename=self.code.co_filename,
            line=self.code.co_firstlineno,
            name=self.code.co_name,
        )
        "The source of the callable"

    @property
    def local_variables(self) -> typing.Tuple[str, ...]:
        """
        Returns the local variables of the function

        Returns
        -------
        tuple
        """
        return self.code.co_names

    @property
    def parameters(self) -> typing.Dict[str, inspect.Parameter]:
        """
        Returns the parameters of the function

        Returns
        -------
        dict
        """
        return self.signature.parameters

    @property
    def return_annotation(self) -> typing.Any:
        """
        Returns the return annotation of the function

        Returns
        -------
        Any
        """
        return self.signature.return_annotation

    @staticmethod
    def get_code(obj: typing.Any) -> types.CodeType:
        """
        Returns the __code__ object of a given callable object.

        Parameters
        ----------
        obj: Any | Callable
            The object to get the __code__ from

        Returns
        -------
        code
        CodeType
            The __code__ object

        Raises
        ------
        TypeError
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
            raise TypeError(
                f"method, function, traceback, frame,                or code object was expected, got {type(obj).__name__}"
            )
        return obj

    # Exposing some of the inspect module functions

    @property
    def is_method(self):
        """Returns whether the callable is a method of an instantiated object or not"""
        return inspect.ismethod(self.callable)

    @property
    def is_function(self):
        """Returns whether the callable is a function or not"""
        return inspect.isfunction(self.callable)

    @property
    def is_class(self):
        """Returns whether the callable is a class or not"""
        return inspect.isclass(self.callable)

    @property
    def source_code(self):
        """Returns the source code for the callable"""
        return inspect.getsource(self.callable)

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
        """
        return f"{self.__class__.__name__}({self.name})"


# Backward compatibility
Function = Callable


class BaseDocumentation:
    """The base docstring parser"""

    original: str
    "Original text"
    description: str
    "The description"

    def __init__(self, docstring: str, flag_prefix: str = "!", **kwargs) -> None:
        """
        Parameters
        ----------
        docstring: str
        flag_prefix: str, default = !
        kwargs
        """
        self.__annotations__ = (
            self.__annotations__ if hasattr(self, "__annotations__") else {}
        )
        "The different type annotations for the class"
        self.extra_arguments = kwargs
        "The extra arguments passed with the docstring parser"
        self.flag_prefix = str(flag_prefix)
        block_map: typing.Dict[str, str] = {}
        inline_map: typing.Dict[str, str] = {}
        flag_map: typing.Dict[str, str] = {}
        for attr, annotation in self.__annotations__.items():
            for mapping, parser in [
                (block_map, parsers.map.MapParser),
                (inline_map, parsers.inline.InlineParser),
                (flag_map, parsers.flag.FlagParser),
            ]:
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
        """
        Cleans the name to normalize it

        Parameters
        ----------
        name: str

        Returns
        -------
        str
        """
        return name.replace(" ", "").upper().strip()

    def dumps(self, indent: int = 4):
        """
        Returns a clean docstring

        Parameters
        ----------
        indent: int, default = 4
        """
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
        """
        Returns
        -------
        str
        """
        representations = [
            f"{attr}={getattr(self, attr)}"
            for attr, annotation in self.__annotations__.items()
            if getattr(self, attr)
            and issubclass(annotation, (parsers.parser.Parser, parsers.flag.FlagParser))
        ]
        return f"{self.__class__.__name__}({', '.join(representations)})"

    @property
    def exported(self):
        """The exported data"""
        results: typing.Dict[str, typing.Any] = {"description": self.description}
        for attr in self.__annotations__:
            result = getattr(self, attr)
            if isinstance(result, parsers.parser.Parser):
                results[attr] = result.exported
            else:
                results[attr] = result
        return results


class ConstantDocumentation(BaseDocumentation):
    """The documentation for a constant"""

    # Flags
    deprecated: parsers.deprecated.Deprecated
    "A flag to indicate if the element is deprecated"
    # Inline Parsers
    notes: parsers.notes.Notes
    "Notes about the element"
    warnings: parsers.warnings.Warnings
    "Warnings about the element"
    important: parsers.important.Important
    "Important notes about the element"
    tips: parsers.tip.Tip
    "Tips about the element"
    caution: parsers.caution.Caution
    "Caution about the element"
    examples: parsers.example.Example
    "Examples of usage"
    # Map Parsers
    changelog: parsers.changelog.Changelog
    "Changelog of the element"
    copyright: parsers.copyright.Copyright
    "Copyright notes for the element"


class Documentation(BaseDocumentation):
    """The full built-in documentation"""

    # Flags
    deprecated: parsers.deprecated.Deprecated
    "A flag to indicate if the element is deprecated"
    # Inline Parsers
    notes: parsers.notes.Notes
    "Notes about the element"
    warnings: parsers.warnings.Warnings
    "Warnings about the element"
    important: parsers.important.Important
    "Important notes about the element"
    tips: parsers.tip.Tip
    "Tips about the element"
    caution: parsers.caution.Caution
    "Caution about the element"
    examples: parsers.example.Example
    "Examples of usage"
    # Map Parsers
    parameters: parsers.parameters.Parameters
    "Parameters for the callable"
    returns: parsers.returns.Returns
    "Return value for the callable"
    yields: parsers.yields.Yields
    "Return value for the callable"
    raises: parsers.raises.Raises
    "Raisable exception by the callable"
    changelog: parsers.changelog.Changelog
    "Changelog of the element"
    copyright: parsers.copyright.Copyright
    "Copyright notes for the element"


# Backward compatibility
Docs = Documentation

