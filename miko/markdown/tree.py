"""
This module contains functions to work with the tree of elements
"""
import ast
import typing

from miko import static


def get_children(root: static.Element, elements: typing.Optional[typing.List[static.Element]] = None):
    elements = elements or []
    # Get all children of an element from the given elements
    results = []
    for node in elements:
        if root.node in node.parents:
            results.append(node)
    return results


def get_direct_children(root: static.Element, elements: typing.List[static.Element]) -> typing.List[static.Element]:
    # Get all direct children of an element from the given elements
    results = []
    for node in elements:
        if not node.parents:
            continue
        try:
            if isinstance(node.node, ast.Name):
                # ast.Name have the assignment as parent
                parent = node.parents[-2]
            else:
                raise ValueError("Internal Error: "
                                 "element is not an assignment")
        except Exception:
            parent = node.parents[-1]
        if parent == root.node:
            results.append(node)
    return results
