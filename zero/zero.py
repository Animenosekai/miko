import typing
import inspect


class Function:
    def __init__(self, func: typing.Callable) -> None:
        self.signature = inspect.signature(func)


class Docs:
    def __init__(self, docs: str, signature: inspect.Signature = None) -> None:
        pass
