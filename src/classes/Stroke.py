from typing import Union

class Stroke:
    def __init__(self,
            color: str,
            thickness: int,
            opacity : Union[int, float] = 1
        ):
        self.color: str = color
        self.width: int = thickness
        self.opacity: Union[int, float] = opacity

    def render(self):
        return f'stroke="{self.color}" stroke-width="{self.width}" stroke-opacity="{self.opacity}"'
