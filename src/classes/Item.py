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
        root = self
        while not(hasattr(root, 'defs_map')):
            root = root.parent
            if root.parent == None:
                break
        # Add other's defs to root -- incase root isn't canvas, if statement will fail
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

    def render_children(self) -> str:
        # Start group for children
        s = ('\t' * self.depth) + f'<g transform="translate({self.position.x}, {self.position.y})"'
        # Check if clipped
        if self.clipped == True:
            s += f' style="clip-path: url(#{id(self)});"'
        s += '>\n'
        for child in self.children:
            s += ('\t' * (self.depth + 1)) + child.render() + '\n'
        s += ('\t' * self.depth) + '</g>'
        return s
