'''
Parser for the `Parameters` paragraph

Example
-------
>>> def func():
...     """
...     Parameters
...     ----------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
import inspect
import json
import typing

from miko.parsers.map import MapElement, MapParser
from miko.utils.caster import try_cast, try_retrieve_type
from miko.utils.empty import Empty, is_empty


class Parameter(MapElement):
    """A parameter in the `Parameters` paragraph"""
    @property
    def signature(self) -> typing.Optional[inspect.Signature]:
        """The signature of the callable, if provided"""
        return self.extra_arguments.get("signature", None)
    
    @property
    def filename(self) -> typing.Optional[str]:
        """The filename where the parameter is defined, if provided"""
        return self.extra_arguments.get("filename", None)

    @property
    def deprecated(self) -> bool:
        """If the parameter is considered as deprecated"""
        return "deprecated" in self.options

    @property
    def signature_parameter(self) -> typing.Optional[inspect.Parameter]:
        """Returns the signature parameter if provided"""
        if not self.signature or not self.name in self.signature.parameters:
            return None

        return self.signature.parameters[self.name]

    @property
    def optional(self) -> bool:
        """If the parameter is optional"""
        if self.signature:
            param = self.signature_parameter
            if param and not is_empty(param.default):
                return True  # it has a default value, thus is optional
        return ("optional" in self.options
                or any(val.startswith("default") for val in self.options))

    @property
    def default(self) -> typing.Union[str, Empty, typing.Any]:
        """
        The default value provided for the given parameter

        Note: This can be something other than a string if the `signature` of the callable is provided
        """
        for opt in self.options:
            if opt.startswith("default"):
                _, _, content = opt.partition("=")
                element = content.strip()
                return try_cast(element, self.types)

        parameter = self.signature_parameter
        if parameter and not is_empty(parameter.default):
            return parameter.default

        return Empty()

    @property
    def types(self) -> typing.Set[typing.Union[str, type, None]]:
        """Returns the parameter's possible types"""
        results = set()

        for option in self.options:
            if option.startswith("default") or option in {"optional", "required", "deprecated"}:
                continue
            results.update(try_retrieve_type(option, filename=self.filename))

        parameter = self.signature_parameter
        if parameter:
            results.update(try_retrieve_type(parameter.annotation, filename=self.filename))

        return results

    def render_options(self) -> str:
        results = []
        types = [element.__name__
                 if hasattr(element, "__name__")
                 else str(element)
                 for element in self.types]
        if types:
            results.append(" | ".join(sorted(types)))

        if self.deprecated:
            results.append("deprecated")

        default = self.default
        if not is_empty(default):
            results.append(f"default = {str(default)}")
        else:
            if self.optional:
                results.append("optional")

        return ", ".join(results)

    @property
    def exported(self):
        try:
            json.dumps(self.default)
        except TypeError:
            if isinstance(self.default, Empty):
                default_value = "@miko.empty"
            else:
                default_value = str(self.default)
        else:
            default_value = self.default
        return {
            **super().exported,
            "deprecated": self.deprecated,
            "optional": self.optional,
            "default": default_value,
            "types": [t.__name__
                      if hasattr(t, "__name__") else str(t)
                      for t in self.types]
        }


class Parameters(MapParser[Parameter]):
    """Parser for the `Parameters` paragraph"""
    element = Parameter
    # element: typing.Type[Parameter] = Parameter
    # elements: typing.List[Parameter]
    names = ["Parameters", "Parameter", "Params",
             "Param", "Arguments", "Argument", "Args", "Arg"]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.signature:
            for parameter in self.signature.parameters:
                parameter = str(parameter)
                if parameter == "self" and self.noself:
                    continue
                if parameter not in self.elements:
                    self[parameter] = self.element(name=parameter,
                                                   **self.extra_arguments)

    @property
    def signature(self) -> typing.Optional[inspect.Signature]:
        """The signature of the callable, if provided"""
        return self.extra_arguments.get("signature", None)

    @property
    def noself(self) -> bool:
        """If the first `self` parameter should be parsed"""
        return self.extra_arguments.get("noself", False)

    def __getitem__(self, key: str) -> Parameter:
        return super().__getitem__(key)

    def __iter__(self):
        return iter(self.elements)
