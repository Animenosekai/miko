import typing

from miko import static

# Tree manipulation

def get_children(root: static.Element, elements: typing.Optional[typing.List[static.Element]] = None):
    elements = elements or []
    # Get all children of an element from the given elements
    results = []
    for node in elements:
        if root.node in node.parents:
            results.append(node)
    return results


def get_direct_children(root: static.Element, elements: typing.Optional[typing.List[static.Element]] = None):
    # Get all direct children of an element from the given elements
    elements = elements or []
    results = []
    for node in elements:
        if node.parents[-1] == root:
            results.append(node)
    return results
