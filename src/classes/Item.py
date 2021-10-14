from typing import Union, List

class Item(object):
    def __init__(self, rotation: Union[int, float] = 0):
        self.rotation: Union[int, float] = rotation
        self.parent: Item = None
        self.children: List[Item] = []
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
