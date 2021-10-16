class Literal:
    def __init__(self, v):
        self.v = v

    def eval(self, pw, ph):
        pass

class Integer(Literal):
    def __str__(self):
        return str(self.v)

class WidthRatio(Literal):
    def __str__(self):
        return str(self.v + "w")

    def eval(self, pw, ph):
        return self.v * pw

class HeightRatio(Literal):
    def __str__(self):
        return str(self.v + "h")
    
    def eval(self, pw, ph):
        return self.v * ph

class BinaryOperator:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def eval(self, pw, ph):
        pass

class Addition(BinaryOperator):
    def __str__(self):
        return "(" + str(self.A) + " + " + str(self.B) + ")"

    def eval(self, pw, ph):
        return self.A.eval(pw, ph) + self.B.eval(pw, ph)

class Subtraction(BinaryOperator):
    def __str__(self):
        return "(" + str(self.A) + " - " + str(self.B) + ")"

    def eval(self, pw, ph):
        return self.A.eval(pw, ph) - self.B.eval(pw, ph)

class Multiplication(BinaryOperator):
    def __str__(self):
        return "(" + str(self.A) + " * " + str(self.B) + ")"

    def eval(self, pw, ph):
        return self.A.eval(pw, ph) * self.B.eval(pw, ph)

class Division(BinaryOperator):
    def __str__(self):
        return "(" + str(self.A) + " + " + str(self.B) + ")"

    def eval(self, pw, ph):
        return self.A.eval(pw, ph) + self.B.eval(pw, ph)

def expression_from_tree(tree):
    # TODO: Make this parse expressions from syntax trees
    return Integer(0) # And update this!