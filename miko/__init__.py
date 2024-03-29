"""
A new Python documentation style

Author
------
Animenosekai
    Original author
"""

from miko.miko import Callable, BaseDocumentation, Documentation, ConstantDocumentation
from miko.miko import Docs, Function  # backward compatibility
from .__info__ import __version__, __license__, __author__, __copyright__  # isort:skip
from . import static, markdown
