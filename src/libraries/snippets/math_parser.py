from math_parser_types import *

def clean_input(s):
    s = s.replace(' ', '')
    s = s.replace('\t', '')
    if len(s) < 2:
        return s, None
    if s[0] == '(' and s[-1] == ')':
        bOpen = 1
        trimmable = True
        for i,c in enumerate(s[1:]):
            if c == '(':
                bOpen += 1
            elif c == ')':
                bOpen -= 1
                if bOpen == 0 and i+1 < len(s)-1:
                    trimmable = False
        if bOpen != 0:
            raise Exception("Bracket mismatch in expression!")
        if trimmable:
            return clean_input(s[1:-1])
    return s

def math_parse(s):
    s = clean_input(s)

    col = 0

    tokens = []
    currentToken = ""

    openBrackets = 0

    while col < len(s):
        c = s[col]
        if c == '(':
            openBrackets += 1
        elif c == ')':
            openBrackets -= 1
        elif c in "+*/":
            if openBrackets == 0:
                if len(currentToken) == 0:
                    raise Exception("Parse error at col " + str(col) + " : empty operand supplied to operator '" + c + "'")
                tokens.append(currentToken)
                tokens.append(c)
                currentToken = ""
            else:
                currentToken += c
        elif c == '-':
            if openBrackets == 0:
                if c != 0 and currentToken not in "*/-+":
                    tokens.append(currentToken)
                    tokens.append(c)
                    currentToken = ""
                else:
                    currentToken += c
            else:
                currentToken += c
        else:
            currentToken += c
        col += 1
    if currentToken != "":
        tokens.append(currentToken)

    maxPrecedence = 0

    print(tokens)

    

f = open("input/math_input.coto", "r")
lines = f.readlines()
f.close()

L = lines[0]
print(math_parse(L))
