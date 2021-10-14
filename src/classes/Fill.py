from typing import Union

class Fill(object):
    def __init__(
            self,
            color: str,
            opacity : Union[int, float]
        ):
        self.color: str = color
        self.opacity: Union[int, float] = opacity

    def render(self) -> str:
        return f'fill="{self.color}" fill-opacity="{self.opacity}"'