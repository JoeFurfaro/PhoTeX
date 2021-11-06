from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from ..Clip import Clip
from .Shape import Shape
from ..util.Vector2 import Vector2
from ..parser.Constants import DEFAULTS

class Polygon(Shape):
    """
    Polygon shape primitive:
    SVG polygons trace a given path and are center alligned be default.
    """
    # create circle as an ellipse with same x and y radius

    def __init__(self,
                 clip: Clip,
                 points: Iterable[Vector2],
                 stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
                 children: Iterable[Item] = [], rotation: Union[int, float] = 0
                 ):
        # calculate center of polygon using points array
        center = Vector2(0, 0)
        for point in points:
            center.x += point.x
            center.y += point.y
        center.x /= len(points)
        center.y /= len(points)
        # set position to center
        super().__init__(clip, center,
                        stroke=stroke, fill=fill,
                        children=children, rotation=rotation)
        self.points = points

    def render(self) -> str:
        # Create polygon SVG instance
        s = '<polygon points="'
        # Add points to SVG
        for index, point in enumerate(self.points):
            s += f'{str(point.x)},{str(point.y)}'
            if index != len(self.points) - 1:
                s += ' '
        # Close points
        s += '" '
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
        s += '<polygon points="'
        for index, point in enumerate(self.points):
            s += f'{str(point.x)},{str(point.y)}'
            if index != len(self.points) - 1:
                s += ' '
        s += '" '
        
        # Apply translation for map since it is relative to parent:
        s += f' transform="translate(-{self.position.x}, -{self.position.y})"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation})"'
        return s + ' />\n</clipPath>'

    def get_height(self) -> Union[int, float]:
        M = max(self.points, key=lambda p: p.y)
        m = min(self.points, key=lambda p: p.y)
        return M.y - m.y

    def get_width(self) -> Union[int, float]:
        M = max(self.points, key=lambda p: p.x)
        m = min(self.points, key=lambda p: p.x)
        return M.x - m.x
