# Shape interface

class Shape(object):
    def validate(self, properties: dict) -> bool:
        raise NotImplementedError

    def rander(self) -> str:
        raise NotImplementedError