# Shape interface

class Shape(object):
    def validate(self, properties: dict) -> bool:
        raise NotImplementedError

    def render(self) -> str:
        raise NotImplementedError