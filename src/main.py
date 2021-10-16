#!/usr/bin/python
import sys
import requests
from classes.parser.Definitions import *
from classes.parser.Generators import *


try:
    from lark import Lark, Tree
except:
    print("Please run `pip install lark Pillow --upgrade` and start the program again")
    exit()

class Parser:
    def __init__(self, grammar : str):
        self.grammar = grammar
        self.defs = DefLookup() # Definition lookup table

    def exception(self, line, col, msg):
        print("Exception on line " + str(line) + " column " + str(col) + ": " + str(msg))
        sys.exit(1)

    def parse(self, code : str):
        try:
            l = Lark(self.grammar)
            parseTree = l.parse(code)
        except Exception as e:
            print(e) # TODO return the error in a nice way
            exit()

        # print(parseTree)

        color_defs = [x for x in parseTree.children if x.data == "color_definition"]
        font_defs = [x for x in parseTree.children if x.data == "font_definition"]
        type_defs = [x for x in parseTree.children if x.data == "type_definition"]
        canvas_defs = [x for x in parseTree.children if x.data == "canvas_definition"]

        self.process_color_defs(color_defs)
        self.process_font_defs(font_defs)
        self.process_type_defs(type_defs)

        # TODO semantic checking

        # TODO build tree

    def process_color_defs(self, color_defs):
        for x in color_defs:
            ID = x.children[0].children[0]
            hex_code = x.children[1].children[0]
            if self.defs.has_color(ID.value):
                self.exception(ID.line, ID.column, ": Color identifier '" + ID.value + "' is already in use")
            self.defs.add(ColorDef(ID.value, hex_code.value))

    def process_font_defs(self, font_defs):
        for x in font_defs:
            ID = x.children[0].children[0]
            font_name = x.children[1].children[0][1:-1]
            font_size = int(x.children[2].children[0])
            font_weight = "regular"
            if len(x.children) > 3:
                font_weight = x.children[3].children[0].value
            if self.defs.has_font(ID):
                self.exception(ID.line, ID.column, ": Font identifier '" + ID.value + "' is already in use")

            # check if fonts exists by sending get to google fonts with the font name
            font_url = 'https://fonts.googleapis.com/css2?family={font_name.replace(" ", "+")}' # we can add params like :wght@100 later
            response = requests.get(font_url)

            if response.status_code != 200:
                self.exception(x.children[1].children[0].line, x.children[1].children[0].column, ": Font family '" + font_name + "' " + font_weight + " could not be found on Google Fonts")
            else:
                print(f'Using font {font_name} from: {font_url}')
            
            self.defs.add(FontDef(ID.value, font_name, font_size, font_weight))

    def process_type_defs(self, type_defs):
        for x in type_defs:
            pass


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
        p = Parser(global_grammar)
        p.parse(code)
    
main()