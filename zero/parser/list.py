from calendar import c
from parser.parser import Parser


class ListElement:
    def __init__(self, options: list = None, content: list = None) -> None:
        self.options = options if options else []
        self.content = content if content else []

    def __repr__(self) -> str:
        return "<ListElement options={options}, content={content} lines>".format(options=", ".join(self.options) if len(self.options) > 1 else "None", content=len(self.content))


class List(Parser):
    __element_type__ = ListElement

    def __init__(self, body: str) -> None:
        super().__init__(body)
        self.elements = {}
        current = None
        for line in self.original.splitlines():
            if line.startswith(" "):
                if current is None:
                    continue
                line = line.strip()
                self.elements[current].content.append(line)
                continue
            name, _, options = line.partition(":")
            current, options = [v.strip() for v in (name, options)]
            if current not in self.elements:
                self.elements[current] = self.__element_type__(options=[opt.strip() for opt in options.split(",")])
            else:
                self.elements[current].options.extend([opt.strip() for opt in options.split(",")])

            print(self.elements)

    def __repr__(self) -> str:
        return "<{name} elements={elements}>".format(name=self.__class__.__name__, elements=len(self.elements))


class Parameter(ListElement):
    def __init__(self, options: list = None, content: list = None) -> None:
        super().__init__(options, content)

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
                return content.strip()
        return None

    @property
    def types(self):
        results = []
        for opt in self.options:
            option = str(opt).lower()
            if option.startswith("default") or option in {"optional", "required"}:
                continue
            results.extend([v.strip() for v in option.split("|")])
        return results

    def __repr__(self) -> str:
        return "<Parameter types={types} optional={optional} default={default}>".format(types=self.types, optional=self.optional, default=self.default)


class Parameters(List):
    __element_type__ = Parameter


class Returns(List):
    pass


class Raises(List):
    pass


class Changelog(List):
    pass


class Copyright(List):
    pass
