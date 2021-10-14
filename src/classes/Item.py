from typing import Union
from collections.abc import Iterable
from .util.Vector2 import Vector2

class Item(object):
    def __init__(self, rotation: Union[int, float] = 0):
        self.rotation: Union[int, float] = rotation
        self.parent: Item = None
        self.children: Iterable[Item] = []
        self.depth: int = 0

    def add_child(self, other) -> None:
        self.children.append(other)
        other.parent = self
        other.depth = self.depth + 1
        sub_children = other.children.copy()
        other.children.clear()
        for sub_child in sub_children:
            other.add_child(sub_child)

    def render(self) -> str:
        raise NotImplementedError

    def render_children(self, center: Vector2, depth: int, children: Iterable) -> str:
        # Start group for children
        s = ('\t' * depth) + f'<g transform="translate({center.x}, {center.y})">\n'
        for child in children:
            s += ('\t' * (depth + 1)) + child.render() + '\n'
        s += ('\t' * depth) + '</g>'
        return s