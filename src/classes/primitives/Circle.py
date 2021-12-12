from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Clip import Clip
from ..Item import Item
from .Shape import Shape
from ..util.Vector2 import Vector2
from ..parser.Constants import DEFAULTS

class Circle(Shape):
    """
    Circle shape primitive:
    SVG circle is center alligned be default.
    """
    # create circle as an ellipse with same x and y radius
    def __init__(self,
            clip: Clip, position: Vector2,
            radius: Union[int, float],
            stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
            children: Iterable[Item] = [], rotation: Union[int, float] = 0
        ):
        super().__init__(clip, position,
                         stroke=stroke, fill=fill,
                         children=children, rotation=rotation)
        self.radius: Union[int, float] = radius

    def render(self) -> str:
        # Create circle SVG instance
        s = f'<circle cx="{self.position.x}" cy="{self.position.y}" r="{self.radius}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"'
        # Apply stroke and fill
        if self.stroke != None:
            s += ' ' + self.stroke.render()
        if self.fill != None:
            s += ' ' + self.fill.render()
        else:
            s += ' ' + f'fill="{DEFAULTS.FILL_COLOR}" fill-opacity="0.0"'
        s += ' />'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            s += self.render_children()
        return s

    def defs(self) -> str:
        # Create defs
        s = super().defs()
        stroke_width = 0 if self.stroke == None else self.stroke.width
        if self.clip != None and self.clip.is_inner():
            s += f'<circle cx="0" cy="0" r="{self.radius}"'
        elif self.clip != None and self.clip.is_outer():
            s += f'<circle cx="0" cy="0" r="{self.radius+stroke_width//2+1}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation})"'
        return s + ' />\n</clipPath>'

    def get_height(self) -> Union[int, float]:
        return self.radius * 2

    def get_width(self) -> Union[int, float]:
        return self.radius * 2
