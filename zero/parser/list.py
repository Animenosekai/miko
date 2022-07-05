import typing
import inspect
from parser.parser import Parser


class ListElement:
    def __init__(self, name: str, options: list = None, content: list = None, signature: inspect.Signature = None) -> None:
        self.name = str(name)
        self.options = options if options else []
        self.content = content if content else []
        self.signature = signature

    def __repr__(self) -> str:
        return "<ListElement options={options}, content={content} lines>".format(options=", ".join(self.options) if len(self.options) > 1 else "None", content=len(self.content))


class List(Parser):
    __element_type__ = ListElement
    __map_attribute__ = "list"

    def __init__(self, body: str = "", signature: inspect.Signature = None) -> None:
        super().__init__(body, signature)
        self.elements = {}
        self.extend(self.original, add_to_original=False)

    def __iter__(self) -> typing.Iterator:
        """
        Returns the iterator.
        """
        return self.elements.values().__iter__()

    def extend(self, content: str, add_to_original: bool = True):
        current = None
        for line in content.splitlines():
            if line.startswith(" "):
                if current is None:
                    continue
                line = line.strip()
                self.elements[current].content.append(line)
                continue
            name, _, options = line.partition(":")
            current, options = [v.strip() for v in (name, options)]
            if current not in self.elements:
                self.elements[current] = self.__element_type__(name=current, options=[opt.strip()
                                                               for opt in options.split(",")], signature=self.signature)
            else:
                self.elements[current].options.extend([opt.strip() for opt in options.split(",")])

        if add_to_original:
            self.original += "\n" + content

    def __repr__(self) -> str:
        return "<{name} elements={elements}>".format(name=self.__class__.__name__, elements=list(self.elements.keys()))

    def __getattr__(self, key: str):
        return self.elements.__getitem__(key)


class Parameter(ListElement):
    @property
    def deprecated(self):
        return "deprecated" in [str(v).lower() for v in self.options]

    @property
    def optional(self):
        options = [str(v).lower() for v in self.options]
        return "optional" in options or any(v.startswith("default") for v in options)

    @property
    def default(self):
        for opt in self.options:
            opt = str(opt)
            if opt.lower().startswith("default"):
                _, _, content = opt.partition("=")
                element = content.strip()
                # i could parse some types here
                return element

        try:
            return self.signature.parameters[self.name].default
        except KeyError:
            return inspect._empty

    @property
    def types(self):
        results = set()
        for opt in self.options:
            option = str(opt).lower()
            if option.startswith("default") or option in {"optional", "required", "deprecated"}:
                continue
            results.update([v.strip() for v in option.split("|")])

        try:
            param = self.signature.parameters[self.name]
            annotation = param.annotation
            if hasattr(annotation, "__origin__") and annotation.__origin__ is typing.Union:
                results.update([str(v) for v in annotation.__args__])
            else:
                results.add(annotation)
        except Exception:
            pass

        return results

    def __repr__(self) -> str:
        return "<Parameter types={types} optional={optional} default={default}>".format(types=self.types, optional=self.optional, default=self.default)


class Parameters(List):
    __element_type__ = Parameter
    __map_attribute__ = "parameters"

    def __init__(self, body: str = "", signature: inspect.Signature = None) -> None:
        super().__init__(body, signature)
        if signature:
            for parameter in signature.parameters:
                parameter = str(parameter)
                if parameter not in self.elements:
                    self.elements[parameter] = self.__element_type__(name=parameter, signature=signature)


class Returns(List):
    __map_attribute__ = "returns"

    def __init__(self, body: str = "", signature: inspect.Signature = None) -> None:
        super().__init__(body, signature)
        if signature:
            annotation = signature.return_annotation
            if hasattr(annotation, "__origin__") and annotation.__origin__ is typing.Union:
                annotations = [str(v) for v in annotation.__args__]
            else:
                annotations = [annotation]
            for annotation in annotations:
                self.elements[annotation] = self.__element_type__(name=annotation)


class Raises(List):
    __map_attribute__ = "raises"


class Changelog(List):
    __map_attribute__ = "changelog"


class Copyright(List):
    __map_attribute__ = "copyright"
