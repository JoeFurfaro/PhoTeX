# USES PYTEST TO RUN UNIT TESTS
from lark import Lark, Tree, Token

## HELPERS #######################
def run_test(code: str, grammarFilePath: str):
    with open(grammarFilePath) as grammar:
        l = Lark(grammar)
        return l.parse(code)

## MATH GRAMMAR ##################
def test_parse_math1():
   assert run_test("5","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '5')])

def test_parse_math2():
   assert run_test("5h","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '5'), Tree('unit', [Token('UNIT', 'h')])])

def test_parse_math3():
   assert run_test("0W","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '0'), Tree('unit', [Token('UNIT', 'W')])])

def test_parse_math4(): # TODO Do we need to limit the size of numbers? 
   assert run_test("12143523642647575887258824686485682457540W","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '12143523642647575887258824686485682457540'), Tree('unit', [Token('UNIT', 'W')])])

def test_parse_math5():
   assert run_test("-3","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '-3')])

def test_parse_math6():
   assert run_test("+3","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '+3')])

def test_parse_math7():
   assert run_test("(12H)","../math_grammar.lark") == Tree('number', [Token('SIGNED_INT', '12'), Tree('unit', [Token('UNIT', 'H')])])

def test_parse_math8():
   assert run_test("(12w+5h)","../math_grammar.lark") == Tree('add', [Tree('number', [Token('SIGNED_INT', '12'), Tree('unit', [Token('UNIT', 'w')])]), Tree('number', [Token('SIGNED_INT', '5'), Tree('unit', [Token('UNIT', 'h')])])])

def test_parse_math9():
   assert run_test("(2+(3+4h*(5w+6w/8)))","../math_grammar.lark") == Tree('add', [Tree('number', [Token('SIGNED_INT', '2')]), Tree('add', [Tree('number', [Token('SIGNED_INT', '3')]), Tree('mul', [Tree('number', [Token('SIGNED_INT', '4'), Tree('unit', [Token('UNIT', 'h')])]), Tree('add', [Tree('number', [Token('SIGNED_INT', '5'), Tree('unit', [Token('UNIT', 'w')])]), Tree('div', [Tree('number', [Token('SIGNED_INT', '6'), Tree('unit', [Token('UNIT', 'w')])]), Tree('number', [Token('SIGNED_INT', '8')])])])])])])

def test_parse_incorrect_math1():
    try:
        run_test("a", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math2():
    try:
        run_test("(((())))", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math3():
    try:
        run_test("(()5", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math4():
    try:
        run_test("2.4", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math5():
    try:
        run_test("w", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math6():
    try:
        run_test("12h+5w", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math6():
    try:
        run_test("(12h+5)w", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math6():
    try:
        run_test(".5", "../math_grammar.lark")
        assert False
    except:
        assert True

def test_parse_incorrect_math6():
    try:
        run_test("++3", "../math_grammar.lark")
        assert False
    except:
        assert True

## DEFINE GRAMMAR ################

## CANVAS GRAMMAR ################
