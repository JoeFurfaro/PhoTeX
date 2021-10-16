from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from ..util.Vector2 import Vector2


class Image(Item):
    def __init__(self,
                 path: str, position: Vector2, size: Vector2,
                 children: Iterable[Item] = [],
                 rotation: Union[int, float] = 0
                 ):
        super().__init__(rotation)
        for child in children:
            self.add_child(child)
        self.path: str = path
        self.position: Vector2 = position
        self.size: Vector2 = size

    def render(self) -> str:
        # Begin Image SVG tag
        s = f'<image x="{self.position.x}" y="{self.position.y}" width="{self.size.x}" height="{self.size.y}" href="{self.path}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"'
        # End Image SVG tag
        s += ' />'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            s += self.render_children()
        return s
