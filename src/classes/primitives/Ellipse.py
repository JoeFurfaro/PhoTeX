from typing import Union, Optional
from collections.abc import Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from .Shape import Shape
from ..util.Vector2 import Vector2


class Ellipse(Shape):
    """
    Ellipse shape primitive:
    SVG ellipse is center alligned be default.
    """
    # create circle as an ellipse with same x and y radius

    def __init__(self,
                 clipped: bool, position: Vector2,
                 rx: Union[int, float], ry: Union[int, float],
                 stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
                 children: Iterable[Item] = [], rotation: Union[int, float] = 0
                 ):
        super().__init__(clipped, position,
                         stroke=stroke, fill=fill,
                         children=children, rotation=rotation)
        self.rx: Union[int, float] = rx
        self.ry: Union[int, float] = ry

    def render(self) -> str:
        # Create circle SVG instance
        s = f'<ellipse cx="{self.position.x}" cy="{self.position.y}" rx="{self.rx}" ry="{self.ry}"'
        # Apply rotation if needed
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"'
        # Apply stroke and fill
        if self.stroke != None:
            s += ' ' + self.stroke.render()
        if self.fill != None:
            s += ' ' + self.fill.render()
        s += ' />'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            s += self.render_children(self.position, self.depth, self.children)
        return s
