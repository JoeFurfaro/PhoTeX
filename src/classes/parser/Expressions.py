from .Constants import *

class Literal:
    def __init__(self, v):
        self.v = v

    def eval(self, pw, ph):
        pass

class Integer(Literal):
    def __str__(self):
        return str(self.v)

    def eval(self, pw, ph):
        return int(self.v)

class WidthRatio(Literal):
    def __str__(self):
        return str(self.v) + UNIT.W.value

    def eval(self, pw, ph):
        return (self.v / 100) * pw

class HeightRatio(Literal):
    def __str__(self):
        return str(self.v) + UNIT.H.value
    
    def eval(self, pw, ph):
        return (self.v / 100) * ph

class BinaryOperator:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def eval(self, pw, ph):
        pass

class UnaryMinus:
    def __init__(self, A):
        self.A = A

    def __str__(self):
        return "(- " + str(self.A) + ")"

    def eval(self, pw, ph):
        return self.A.eval(pw, ph) * -1

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
        return "(" + str(self.A) + " / " + str(self.B) + ")"

    def eval(self, pw, ph):
        return int(self.A.eval(pw, ph) / self.B.eval(pw, ph))

def expression_from_tree(tree):
    return expression_from_subtree(tree.children[0])

def expression_from_subtree(tree):
    T = tree.data
    if T == "value": #TODO unhardcode
        v = tree.children[0]
        value = int(v.value)
        if len(tree.children) == 1:
            return Integer(value)
        else:
            unit = tree.children[1].children[0].value
            if unit == UNIT.H.value:
                return HeightRatio(value)
            elif unit == UNIT.W.value:
                return WidthRatio(value)
    elif T == "add":
        return Addition(expression_from_subtree(tree.children[0]), expression_from_subtree(tree.children[1]))
    elif T == "sub":
        return Subtraction(expression_from_subtree(tree.children[0]), expression_from_subtree(tree.children[1]))
    elif T == "mul":
        return Multiplication(expression_from_subtree(tree.children[0]), expression_from_subtree(tree.children[1]))
    elif T == "div":
        return Division(expression_from_subtree(tree.children[0]), expression_from_subtree(tree.children[1]))
    elif T == "neg":
        return UnaryMinus(expression_from_subtree(tree.children[0]))

def find_in_tree(tree, key):
    for x in tree.children:
        if x.data == key:
            return x.children
    return None