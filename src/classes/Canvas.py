from typing import Union, Dict, Iterable
from .Item import Item
from .util.Vector2 import Vector2
from .Font import Font
from .primitives.Shape import Shape
from .primitives.Text import Text
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from cairosvg import svg2png

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
        self.file_name: str = file_name
        self.file_format: str = file_format
        self.canvas_size: Vector2 = size
        self.defs_map: Dict[str, str] = {}
        for child in children:
            self.add_child(child)

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

    def add_child(self, other) -> None:
        if hasattr(other, 'position'):
            # Shift position of immediate children
            other.position.x += self.canvas_size.x // 2
            other.position.y += self.canvas_size.y // 2
        return super().add_child(other)

    def export(self):
        svg_file: str = self.file_name + '.svg'
        export_file: str = self.file_name + '.' + self.file_format
        # An svg file will always be exported first
        with open(svg_file, 'w') as fh:
            fh.write(self.render())
        # Export the svg to whatever file type they specified
        if self.file_format != "svg":
            svg2png(bytestring=self.render(),write_to=self.file_name + ".png")


    def add_def(self, other: Union[Font, Shape, Text]):
        if len(other.defs()) > 0 and (isinstance(other, Font) or isinstance(other, Shape) or isinstance(other, Text)):
            if isinstance(other, Font):
                self.defs_map[other.family] = other.defs()
            elif isinstance(other, Text):
                # get font from text and add to defs
                self.defs_map[other.font.family] = other.font.defs()
            elif isinstance(other, Shape) and other.clipped == True:
                self.defs_map[id(other)] = other.defs()
