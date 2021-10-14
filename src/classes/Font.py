class Font(object):
    def __init__(self,
            name: str,
            size: int,
            weight: str
        ):
        self.name: str = name
        self.size: int = size
        self.weight: str = weight