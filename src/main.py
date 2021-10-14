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

    with open(fileToParse) as fileContents, open("global_grammar.lark") as global_grammar:

        code = str(fileContents.read()) + "\n" # add a new line to ease grammar checking (NOTE: breaks math grammar when it is by itself)

        try:
            parseTree = parseCode(code, global_grammar)
        except Exception as e:
            print(e) # TODO return the error in a nice way
            exit()

        print(parseTree)

        color_defs = [x for x in parseTree.children if x.data == "color_definition"]
        font_defs = [x for x in parseTree.children if x.data == "font_definition"]
        type_defs = [x for x in parseTree.children if x.data == "type_definition"]
        canvas_defs = [x for x in parseTree.children if x.data == "canvas_definition"]

        # TODO semantic checking

        # TODO build tree

def parseCode(code: str, grammar: str):
    l = Lark(grammar)

    output = l.parse(code)

    return output
    
main()