'''
Parser for the `Copyright` paragraph

Example
-------
>>> def func():
...     """
...     Copyright
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
'''
import typing
from miko.parsers.map import MapParser, MapElement


class License(MapElement):
    """A license in the `Copyright` section"""
    @property
    def license(self) -> typing.Optional[str]:
        for option in self.options:
            if option.startswith(("year", "from", "to")):
                continue
            return option
        return None

    @property
    def year_from(self) -> typing.Optional[int]:
        for option in self.options:
            if not option.startswith("from"):
                continue
            return int(option.partition("=")[2])
        for option in self.options:
            if not option.startswith("year"):
                continue
            return int(option.partition("=")[2])
        return None

    @property
    def year_to(self) -> typing.Optional[int]:
        for option in self.options:
            if not option.startswith("to"):
                continue
            return int(option.partition("=")[2])
        for option in self.options:
            if not option.startswith("year"):
                continue
            return int(option.partition("=")[2])
        return None

    def render_options(self) -> str:
        results = []
        if self.license:
            results.append(self.license)
        if self.year_from == self.year_to:
            results.append(f"year = {self.year_from}")
        else:
            results.append(f"from = {self.year_from}")
            results.append(f"to = {self.year_to}")
        return ", ".join(results)

    @property
    def exported(self):
        return {
            **super().exported,
            "license": self.license,
            "from": self.year_from,
            "to": self.year_to
        }


class Copyright(MapParser):
    """Parser for the `Copyright` paragraph"""
    names = ["Copyright", "Copyrights", "Authors", "Author"]
