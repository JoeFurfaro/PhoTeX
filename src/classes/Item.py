from typing import Union, Iterable
from .util.Vector2 import Vector2

class Item(object):
    def __init__(self, rotation: Union[int, float] = 0):
        self.rotation: Union[int, float] = rotation
        self.parent: Item = None
        self.children: Iterable[Item] = []
        self.depth: int = 0

    def add_child(self, other) -> None:
        # Get root of entire tree -- Should be Canvas
        root = self.parent
        while not(hasattr(root, 'defs_map')):
            if root.parnet == None:
                break
            root = root.parent
        # Add other's defs to root
        if hasattr(root, 'defs_map'):
            root.add_def(other)
        # Add other to children
        self.children.append(other)
        # Set other's parent to current item
        other.parent = self
        other.depth = self.depth + 1 # update depth of other
        sub_children = other.children.copy() # copy children of other
        other.children.clear() # delete children of other
        # Reupdate all children of other using this algorithm
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
