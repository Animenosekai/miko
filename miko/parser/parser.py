"""
Defines the base parser
"""
import inspect


class Parser:
    """
    The base class for the parsers
    """
    __map_attribute__ = "parser"

    def __init__(self, body: str = "", signature: inspect.Signature = None, **kwargs) -> None:
        """
        Parameters
        ----------
        body: str, default = ""
        signature: inspect.Signature, default = None
        **kwargs

        Returns
        -------
        None
        """
        self.original = str(body)
        self.signature = signature

    def as_dict(self, camelCase: bool = False):
        """
        Parameters
        ----------
        camelCase: bool, default = False
        """
        return {
            "original": self.original
        }
