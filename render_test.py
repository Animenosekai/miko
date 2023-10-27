import ast
from rich.console import Console
from miko.static import get_elements
from miko.renderer.render import make_constant_docs

with open("test.py") as f:
    r = ast.parse(f.read())
c = Console()

with open("test.md", "w") as f:
    f.write(make_constant_docs(get_elements(r)[1], "test.py", base_dir="."))
