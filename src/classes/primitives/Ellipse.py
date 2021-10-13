import Shape

class Ellipse(Shape):
    def __init__(self, position : tuple, x_radius : float, y_radius : float):
        self.position = position
        self.xR = x_radius
        self.yR = y_radius
