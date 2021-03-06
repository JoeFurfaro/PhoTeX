from typing import Union, Optional, Iterable
from ..Stroke import Stroke
from ..Fill import Fill
from ..Clip import Clip
from ..Item import Item
from ..util.Vector2 import Vector2

class Shape(Item):
    def __init__(self,
            clip: Clip, position: Vector2,
            stroke: Optional[Stroke] = None, fill: Optional[Fill] = None,
            children: Iterable[Item] = [],
            rotation: Union[int, float] = 0
        ):
        super().__init__(rotation)
        for child in children:
            self.add_child(child)
        self.clip: Clip = clip
        self.position: Vector2 = position
        self.stroke: Optional[Stroke] = stroke
        self.fill: Optional[Fill] = fill

    def render(self) -> str:
        raise NotImplementedError

    def defs(self) -> str:
        return f'<clipPath id="{id(self)}" clipPathUnits="userSpaceOnUse">\n\t'

    def get_height(self) -> Union[int, float]:
        raise NotImplementedError

    def get_width(self) -> Union[int, float]:
        raise NotImplementedError
