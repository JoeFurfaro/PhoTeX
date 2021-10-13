#!/usr/bin/python

import sys
try:
    from lark import Lark, Tree
except:
    print("Please run `pip install lark --upgrade` and start the program again")
    exit()

def main():
    fileToParse = ""
    if len(sys.argv) == 1:
        fileToParse = input("Enter file name: ")
    elif len(sys.argv) == 2:
        fileToParse = sys.argv[1]
    else:
        print("Please only pass up to one argument (the file to parse) to this command.")
        exit()

    with open(fileToParse) as fileContents, open("math_grammar.lark") as mathgrammar: # TODO build all grammar into one file

        code = str(fileContents.read()) + "\n" # add a new line to ease grammar checking (NOTE: breaks math grammar when it is by itself)

        try:
            parseTree = parseCode(code, mathgrammar)
        except:
            print("Error in the file") # TODO return the error in a nice way
            exit()

        print(parseTree)

        # TODO semantic checking

        # TODO build tree

def parseCode(code: str, grammar: str):
    l = Lark(grammar)

    output = l.parse(code)

    return output
    
main()