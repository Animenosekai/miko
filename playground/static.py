"""Static Analysis of Python Code"""
import argparse
import ast
import dataclasses
import pathlib
import typing


@dataclasses.dataclass
class Scope:
    depth: list[str]
    variables: dict[str, ast.AST]


def analyze(tree: ast.AST, scope: typing.Optional[Scope] = None):
    """
    Analyzes the AST

    Parameters
    ----------
    tree: AST
    scope: ForwardRef('Scope') | NoneType, default = None
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to file to analyze')
    args = parser.parse_args()
    path = pathlib.Path(args.path)
    data = path.read_text()
    tree = ast.parse(data)
    analyze(tree)

