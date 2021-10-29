from typing import Union, Optional, Iterable
from .Shape import Shape
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from ..util.Vector2 import Vector2

class Rect(Shape):
    """
    Rectangle shape primitive:
    SVG rect is positioned at the top left, so we must adjust coordinates:
    - cx = x - width//2
    - cy = y - height//2
    """
    def __init__(self,
            clip: bool, position: Vector2,
            width: Union[int, float], height: Union[int, float],
            stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
            children: Iterable[Item] = [], rotation: Union[int, float] = 0
        ):
        super().__init__(clip, position,
                         stroke=stroke, fill=fill,
                         children=children, rotation=rotation)
        self.width: Union[int, float] = width
        self.height: Union[int, float] = height

    def render(self) -> str:
        rx = self.position.x - (self.width // 2)
        ry = self.position.y - (self.height // 2)
        # Create rectangle SVG instance
        s = f'<rect x="{rx}" y="{ry}" width="{self.width}" height="{self.height}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"'
        # Apply stroke and fill
        if self.stroke != None:
            s += ' ' + self.stroke.render()
        if self.fill != None:
            s += ' ' + self.fill.render()
        else:
            s += ' ' + 'fill="#000000" fill-opacity="0.0"'
        s += ' />'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            s += self.render_children()
        return s

    def defs(self) -> str:
        s = super().defs()
        stroke_width = 0 if self.stroke == None else self.stroke.width
        if self.clip != None and self.clip.is_inner():
            s += f'<rect x="{-(self.width // 2) + (stroke_width // 2)}" y="{-(self.height // 2) + (stroke_width // 2)}" width="{self.width - stroke_width}" height="{self.height - stroke_width}"'
        elif self.clip != None and self.clip.is_outer():
            s += f'<rect x="{-(self.width // 2) - (stroke_width // 2)-1}" y="{-(self.height // 2) - (stroke_width // 2)-1}" width="{self.width + stroke_width}+2" height="{self.height + stroke_width}+2"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation})"'
        return s + ' />\n</clipPath>'

    def get_height(self) -> Union[int, float]:
        return self.height

    def get_width(self) -> Union[int, float]:
        return self.width
