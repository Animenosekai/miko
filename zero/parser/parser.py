import inspect


class Parser:
    __map_attribute__ = "parser"

    def __init__(self, body: str = "", signature: inspect.Signature = None, **kwargs) -> None:
        self.original = str(body)
        self.signature = signature

    def as_dict(self, camelCase: bool = False):
        return {
            "original": self.original
        }
