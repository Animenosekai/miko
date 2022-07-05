import inspect


class Parser:
    __map_attribute__ = "parser"

    def __init__(self, body: str = "", signature: inspect.Signature = None) -> None:
        self.original = str(body)
        self.signature = signature
