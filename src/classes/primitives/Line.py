from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from .Shape import Shape
from ..util.Vector2 import Vector2

class Line(Shape):

    def __init__(self,
            clipped: bool,
            start: Vector2, end: Vector2,
            stroke: Optional[Stroke] = None,
            children: Iterable[Item] = [], rotation: Union[int, float] = 0
        ):
        position = (end - start) * 2 + start
        super().__init__(clipped, position,
                         stroke=stroke, fill=None,
                         children=children, rotation=rotation)
        self.start: Vector2 = start
        self.end: Vector2 = end

    def render(self) -> str:
        s = f'<line x1="{self.start.x}" y1="{self.start.y}" x2="{self.start.x}" y2="{self.start.y}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"'
        # Apply stroke
        if self.stroke != None:
            s += ' ' + self.stroke.render()
        s += ' />'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            s += self.render_children(self.position, self.depth, self.children)
        return s