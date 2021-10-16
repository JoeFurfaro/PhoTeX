from typing import Union, Dict, Iterable
from .Item import Item
from .util.Vector2 import Vector2
from .Font import Font
from .primitives.Shape import Shape

class Canvas(Item):
    """
    Top-Level class for the Canvas tree.
    In SVG, the Canvas is the root of the file, and would be equivalent to the SVG root element.

    ```svg
    <svg height="h" width="w">
        ...
    </svg>
    ```
    """
    def __init__(self,
            file_name: str, file_format: str, size: Vector2,
            children: Iterable[Item] = [],
            rotation: Union[int, float] = 0
        ):
        super().__init__(rotation)
        for child in children:
            self.add_child(child)
        self.file_name: str = file_name
        self.file_format: str = file_format
        self.canvas_size: Vector2 = size
        self.defs_map: Dict[str, str] = {}

    def render(self) -> str:
        """
        Render the Canvas to its SVG equivalent.
        """
        # Set-Up svg tag
        s = f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{self.canvas_size.x}" height="{self.canvas_size.y}"'
        if abs(self.rotation) > 1e-6:
             s += f' transform="rotate({self.rotation} {self.canvas_size.x // 2} {self.canvas_size.y // 2})"'
        s += '>\n'
        # Render global defs
        if self.defs_map != {}:
            s += '\t<defs>\n'
            for key, value in self.defs_map.items():
                for line in value.split('\n'):
                    s += f'\t\t{line}\n'
            s += '\t</defs>\n'
        # Render children
        for child in self.children:
            s += '\t' + child.render() +'\n'
        # Close svg tag and return string
        return s + '</svg>'

    def add_def(self, other: Union[Font, Shape]):
        if len(other.defs()) > 0 and (isinstance(other, Font) or isinstance(other, Shape)):
            if isinstance(other, Font):
                self.defs_map[other.family] = other.defs()
            elif isinstance(other, Shape) and other.clipped == True:
                self.defs_map[id(other)] = other.defs()
