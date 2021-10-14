from typing import Union, Optional
from collections.abc import Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Item import Item
from .Shape import Shape
from ..util.Vector2 import Vector2

class Rect(Shape):
    """
    Rectangle shape primitive:
    - position: Vector2
        - x and y integers representing the position of the rectangle's center
    - width and height integers representing the width and height of the rectangle

    SVG rect is positioned at the top left, so we must adjust coordinates:
    - cx = x - width//2
    - cy = y - height//2
    """
    def __init__(self,
            children: Iterable[Item],
            clipped: bool, position: Vector2,
            width: int, height: int,
            stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
            rotation: Union[int, float] = 0):
        super().__init__(children, clipped, position,
            stroke=stroke, fill=fill, rotation=rotation)
        self.width: int = width
        self.height: int = height

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
        s += ' />'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            # Start group for children
            print(str(self.depth))
            s += ('\t' * self.depth) + '<g>\n'
            for child in self.children:
                s += ('\t' * (self.depth + 1)) + child.render() + '\n'
            s += ('\t' * self.depth) + '</g>\n'
        return s
