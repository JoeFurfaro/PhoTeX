from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from ..Clip import Clip
from .Shape import Shape
from ..util.Vector2 import Vector2

class Line(Shape):
    def __init__(self,
            clip: Clip,
            start: Vector2, end: Vector2,
            stroke: Stroke,
            children: Iterable[Item] = [], rotation: Union[int, float] = 0
        ):
        position = (end - start) * 2 + start
        super().__init__(clip, position,
                         stroke=stroke, fill=None,
                         children=children, rotation=rotation)
        self.start: Vector2 = start
        self.end: Vector2 = end

    def render(self) -> str:
        s = f'<line x1="{self.start.x}" y1="{self.start.y}" x2="{self.end.x}" y2="{self.end.y}"'
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
            s += self.render_children()
        return s

    def defs(self) -> str:
        # Create defs
        s = super().defs()
        s += f'<line x1="-{self.start.x}" y1="-{self.start.y}" x2="-{self.start.x}" y2="-{self.start.y}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation})"'
        return s + ' />\n</clipPath>'

    def get_height(self) -> Union[int, float]:
        return max(self.start.y, self.end.y) - min(self.start.y, self.end.y)

    def get_width(self) -> Union[int, float]:
        return max(self.start.x, self.end.x) - min(self.start.x, self.end.x)
