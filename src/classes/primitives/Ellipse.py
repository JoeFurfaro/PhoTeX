from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from ..Clip import Clip
from .Shape import Shape
from ..util.Vector2 import Vector2


class Ellipse(Shape):
    """
    Ellipse shape primitive:
    SVG ellipse is center alligned be default.
    """
    # create circle as an ellipse with same x and y radius

    def __init__(self,
                 clip: Clip, position: Vector2,
                 rx: Union[int, float], ry: Union[int, float],
                 stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
                 children: Iterable[Item] = [], rotation: Union[int, float] = 0
                 ):
        super().__init__(clip, position,
                         stroke=stroke, fill=fill,
                         children=children, rotation=rotation)
        self.rx: Union[int, float] = rx
        self.ry: Union[int, float] = ry

    def render(self) -> str:
        # Create ellipse SVG instance
        s = f'<ellipse cx="{self.position.x}" cy="{self.position.y}" rx="{self.rx}" ry="{self.ry}"'
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
        # Create defs
        s = super().defs()
        stroke_width = 0 if self.stroke == None else self.stroke.width
        if self.clip != None and self.clip.is_inner():
            s += f'<ellipse cx="0" cy="0" rx="{self.rx-stroke_width//2}" ry="{self.ry-stroke_width//2}"'
        elif self.clip != None and self.clip.is_outer():
            s += f'<ellipse cx="0" cy="0" rx="{self.rx+stroke_width//2+1}" ry="{self.ry+stroke_width//2+1}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation})"'
        return s + ' />\n</clipPath>'

    def get_height(self) -> Union[int, float]:
        return self.ry * 2

    def get_width(self) -> Union[int, float]:
        return self.rx * 2
