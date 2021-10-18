from enum import Enum
from typing import Union, Optional, Iterable
from ..Item import Item
from ..Stroke import Stroke
from ..Fill import Fill
from ..Font import Font
from ..util.Vector2 import Vector2

class Anchor(Enum):
    """
    Horizontal Anchor Points for Text
    """
    LEFT = "start"
    CENTER = "middle"
    RIGHT = "end"

class Baseline(Enum):
    """
    Vertical Anchor Points for Text
    """
    TOP = "hanging"
    CENTER = "middle"
    BOTTOM = "baseline"

class Text(Item):
    def __init__(self,
                 text: str,
                 position: Vector2,
                 width: Optional[int] = None,
                 halign: Anchor = Anchor.CENTER,
                 valign: Baseline = Baseline.CENTER,
                 font: Optional[Font] = None,
                 stroke: Optional[Stroke] = None,
                 fill: Optional[Fill] = None,
                 children: Iterable[Item] = [],
                 rotation: Union[int, float] = 0,
        ):
        super().__init__(rotation)
        for child in children:
            self.add_child(child)
        self.text: str = text
        self.position: Vector2 = position
        self.width: Optional[int] = width
        self.anchor: Anchor = halign
        self.baseline: Baseline = valign
        self.font: Optional[Font] = font
        self.fill: Optional[Fill] = fill
        self.stroke: Optional[Stroke] = stroke

    def render(self) -> str:
        # Begin Text SVG tag
        s = f'<text x="{self.position.x}" y="{self.position.y}" text-anchor="{self.anchor.value}" alignment-baseline="{self.baseline.value}"'
        # Apply text-length if width is specified
        if self.width != None:
            s += f' textLength="{self.width}"'
        # Get font properties
        if self.font != None:
            s += ' ' + self.font.render()
        # Get fill properties
        if self.fill != None:
            s += ' ' + self.fill.render()
        # Get stroke properties
        if self.stroke != None:
            s += ' ' + self.stroke.render()
        # Get rotation properties
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation} {self.position.x} {self.position.y})"'
        # SVG text contents
        s += f'>{self.text}</text>'
        # Render Children
        if len(self.children) > 0:
            s += '\n'
            s += self.render_children()
        return s

    def defs(self):
        # Create defs
        s = f'<clipPath id="{id(self)}">\n\t'
        s += f'<text x="-{self.position.x}" y="-{self.position.y}" text-anchor="{self.anchor.value}" alignment-baseline="{self.baseline.value}"'
        # Apply text-length if width is specified
        if self.width != None:
            s += f' textLength="{self.width}"'
        # Get rotation properties
        if abs(self.rotation) > 1e-6:
            s += f' transform="rotate({self.rotation})"'
        s += f'>{self.text}</text>\n</clipPath>'
        return s

    def get_height(self) -> Union[int, float]:
        raise NotImplementedError

    def get_width(self) -> Union[int, float]:
        return self.width if self.width != None else len(self.text)
