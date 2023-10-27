import ast
from rich.console import Console
from miko import static
from miko.renderer.render import make_constant_docs, render_heading

with open("test.py") as f:
    r = ast.parse(f.read())
c = Console()

with open("test.md", "w") as f:
    results = [render_heading("Constants", 1)]
    for element in static.get_elements(r):
        if isinstance(element, static.ConstantElement):
            results.append(make_constant_docs(element, "test.py", parent_path="miko.test",
                                              level=1, base_dir="."))
    f.write("\n".join(results))
