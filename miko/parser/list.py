import inspect
import typing

from miko.parser.parser import Parser


class ListElement:
    def __init__(self, name: str, options: list = None, content: list = None, signature: inspect.Signature = None) -> None:
        self.name = name.__name__ if isinstance(name, type) else str(name)
        self.options = [v for v in options if v] if options else []
        self.content = [c for c in content if c] if content else []
        self.signature = signature

    def __repr__(self) -> str:
        return "<ListElement options={options}, content={content} lines>".format(options=", ".join(self.options) if len(self.options) > 1 else "None", content=len(self.content))

    def as_dict(self, camelCase: bool = False):
        return {
            "name": self.name,
            "options": self.options,
            "content": self.content
        }


class List(Parser):
    __element_type__ = ListElement
    __map_attribute__ = "list"

    def __init__(self, body: str = "", signature: inspect.Signature = None, **kwargs) -> None:
        super().__init__(body, signature)
        self.elements = {}
        self.extend(self.original, add_to_original=False)

    def __iter__(self) -> typing.Iterator:
        """
        Returns the iterator.
        """
        return self.elements.values().__iter__()

    def __len__(self):
        return len(self.elements)

    def as_dict(self, camelCase: bool = False):
        results = super().as_dict(camelCase)
        results.update({
            "elements": {str(k) if camelCase else k: v.as_dict(camelCase) for k, v in self.elements.items()}
        })
        return results

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
    def deprecated(self) -> bool:
        return "deprecated" in [str(v).lower() for v in self.options]

    @property
    def optional(self) -> bool:
        options = [str(v).lower() for v in self.options]
        return "optional" in options or any(v.startswith("default") for v in options)

    @property
    def default(self) -> typing.Optional[str]:
        for opt in self.options:
            opt = str(opt)
            if opt.lower().startswith("default"):
                _, _, content = opt.partition("=")
                element = content.strip()
                # i could parse some types here
                return element

        try:
            result = self.signature.parameters[self.name].default
            if not isinstance(result, inspect._empty) and not result is inspect._empty:
                return result.__name__ if isinstance(result, type) else str(result)
        except Exception:
            return None

    @property
    def types(self) -> set:
        results = set()
        for opt in self.options:
            option = str(opt).lower()
            if option.startswith("default") or option in {"optional", "required", "deprecated"}:
                continue
            results.update([v.strip() for v in str(opt).split("|") if str(v).strip().replace(" ", "") != "<class'inspect._empty'>"])

        try:
            param = self.signature.parameters[self.name]
            annotation = param.annotation
            if annotation is not inspect._empty and str(annotation).strip().replace(" ", "") != "<class 'inspect._empty'>":
                if hasattr(annotation, "__origin__") and annotation.__origin__ is typing.Union:
                    for a in annotation.__args__:
                        if str(a).lower().strip('"').strip("'").strip() not in {str(r).lower() for r in results}:
                            results.add(a)
                elif annotation:
                    if str(annotation).lower().strip('"').strip("'").strip() not in {str(r).lower() for r in results}:
                        results.add(annotation)
        except Exception:
            pass

        return results

    def __repr__(self) -> str:
        return "<Parameter types={types} optional={optional} default={default}>".format(types=self.types, optional=self.optional, default=self.default)

    def as_dict(self, camelCase: bool = False):
        results = super().as_dict(camelCase)
        results.update({
            "types": [str(t) for t in self.types] if camelCase else self.types,
            "optional": self.optional,
            "default": self.default,
            "deprecated": self.deprecated
        })
        return results


class Parameters(List):
    __element_type__ = Parameter
    __map_attribute__ = "parameters"

    def __init__(self, body: str = "", signature: inspect.Signature = None, noself: bool = False, **kwargs) -> None:
        super().__init__(body, signature)
        if signature:
            for parameter in signature.parameters:
                parameter = str(parameter)
                if parameter == "self" and noself:
                    continue
                if parameter not in self.elements:
                    self.elements[parameter] = self.__element_type__(name=parameter, signature=signature)


class Returns(List):
    __map_attribute__ = "returns"

    def __init__(self, body: str = "", signature: inspect.Signature = None, **kwargs) -> None:
        super().__init__(body, signature)
        if signature:
            annotation = signature.return_annotation
            if hasattr(annotation, "__origin__") and annotation.__origin__ is typing.Union:
                annotations = [str(v) for v in annotation.__args__]
            else:
                annotations = [annotation]
            for annotation in annotations:
                if annotation not in self.elements and not isinstance(annotation, inspect._empty) and not annotation is inspect._empty:
                    self.elements[annotation] = self.__element_type__(name=annotation)


class Raises(List):
    __map_attribute__ = "raises"


class Changelog(List):
    __map_attribute__ = "changelog"


class Copyright(List):
    __map_attribute__ = "copyright"
