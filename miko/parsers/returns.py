'''
Parser for the `Returns` paragraph

Example
-------
>>> def func():
...     """
...     Returns
...     -------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
import inspect
import typing

from miko.parsers.map import MapParser
from miko.utils.caster import try_retrieve_type


class Returns(MapParser):
    """Parser for the `Returns` paragraph"""
    names = ["Returns", "Return", "Returning"]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.signature:
            annotation = self.signature.return_annotation
            annotations = try_retrieve_type(annotation)
            for annotation in annotations:
                if annotation and not annotation in self.elements:
                    if hasattr(annotation, "__name__"):
                        name = annotation.__name__
                    else:
                        name = str(annotation)
                    self[name] = self.element(name=name,
                                              **self.extra_arguments)

    @property
    def signature(self) -> typing.Optional[inspect.Signature]:
        """The signature of the callable, if provided"""
        return self.extra_arguments.get("signature", None)
