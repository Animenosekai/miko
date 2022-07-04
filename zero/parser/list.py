from calendar import c
from parser.parser import Parser


class ListElement:
    pass


class List(Parser):
    def __init__(self, body: str) -> None:
        super().__init__(body)
        self.elements = {}
        current = None
        for line in self.original.splitlines():
            if line.startswith(" "):
                if current is None:
                    continue
                line = line.strip()
                self.elements[current]["content"].append(line)
                continue
            name, _, options = line.partition(":")
            current, options = [v.strip() for v in (name, options)]
            if current not in self.elements:
                self.elements[current] = {"options": [opt.strip() for opt in options.split(",")], "content": []}
            else:
                self.elements[current]["options"].extend([opt.strip() for opt in options.split(",")])

        print("self.elements", self.elements)

class Parameters(List):
    pass


class Returns(List):
    pass


class Raises(List):
    pass


class Changelog(List):
    pass


class Copyright(List):
    pass
