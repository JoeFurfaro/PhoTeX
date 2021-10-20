#!/usr/bin/python
import sys
import os
import requests
from classes.parser.Definitions import *
from classes.parser.Generators import *
from classes.parser.Expressions import *


try:
    from lark import Lark, Tree
    import PIL
    from svglib.svglib import svg2rlg
except:
    print("Please run `pip install lark Pillow svglib --upgrade` and start the program again")
    exit()

class Parser:
    def __init__(self, grammar : str):
        self.grammar = grammar
        self.defs = DefLookup() # Definition lookup table

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
        print("Registered " + str(len(self.defs.colors)) + " color definition(s)")
        self.process_font_defs(font_defs)
        print("Registered " + str(len(self.defs.fonts)) + " font definition(s)")
        self.process_type_defs(type_defs)
        print("Registered " + str(len(self.defs.types)) + " custom type definition(s)")
        
        for c in canvas_defs:
            file_token = c.children[0].children[0]
            file_name = c.children[0].children[0][1:-1]
            width = int(c.children[1].children[0].children[0].children[0])
            height = int(c.children[1].children[1].children[0].children[0])

            base = os.path.splitext(file_name)[0]
            ext = os.path.splitext(file_name)[1][1:]

            # IN A RUSH! TODO: BETTER FILE NAME VALIDATION (using regex?)

            if ext.lower() not in ("png", "svg", "jpg", "jpeg"):
                Generator.exception(file_token.line, file_token.column, ": Canvas name must have extension SVG, PNG, or JPG")

            if self.defs.has_canvas(file_name):
                Generator.exception(file_token.line, file_token.column, ": Canvas name '" + file_name + "' is already in use")

            print("Found canvas with name '" + file_name + "'. Creating generators... ")
            children_generators = Generator.from_item_list(Generator.find_in_tree(c, "item_list"), self.defs)

            self.defs.add(CanvasDef(base, ext.lower(), width, height, children_generators))

        for canvas in self.defs.canvases:
            print("Generators constructed. Generating objects for canvas '" + canvas.name + "'...")
            canvas.generate()

            print("Done generating objects for '" + canvas.name + "'. Building output...")

            # TODO: Build SVG!
            c = Canvas(canvas.base, canvas.ext.lower(), Vector2(canvas.width, canvas.height), canvas.children, 0)
            c.export()

            print("Built canvas '" + canvas.name + "!")

        print("Successfully built " + str(len(self.defs.canvases)) + " canvas(es)! Compilation complete.")


    def process_color_defs(self, color_defs):
        for x in color_defs:
            ID = x.children[0].children[0]
            hex_code = x.children[1].children[0]
            if self.defs.has_color(ID.value):
                Generator.exception(ID.line, ID.column, ": Color identifier '" + ID.value + "' is already in use")
            self.defs.add(ColorDef(ID.value, hex_code.value))

    def process_font_defs(self, font_defs):
        for x in font_defs:
            ID = x.children[0].children[0]
            font_name = x.children[1].children[0][1:-1]
            font_size = int(x.children[2].children[0])
            font_weight = "regular"
            if len(x.children) > 3:
                font_weight = x.children[3].children[0].value
            if self.defs.has_font(ID.value):
                Generator.exception(ID.line, ID.column, ": Font identifier '" + ID.value + "' is already in use")

            # check if fonts exists by sending get to google fonts with the font name
            font_url = 'https://fonts.googleapis.com/css2?family={font_name.replace(" ", "+")}' # we can add params like :wght@100 later
            response = requests.get(font_url)

            if response.status_code != 200:
                # Generator.exception(x.children[1].children[0].line, x.children[1].children[0].column, ": Font family '" + font_name + "' " + font_weight + " could not be found on Google Fonts")
                pass
            else:
                print(f'Using font {font_name} from: {font_url}')
            
            self.defs.add(FontDef(ID.value, font_name, font_size, font_weight))

    def process_type_defs(self, type_defs):
        for x in type_defs:
            ID = x.children[0].children[0]
            width = None
            height = None
            w_tree = Generator.find_in_tree(x, "int_width")
            if w_tree != None:
                width = Generator.find_in_tree(x, "int_width")[0]
                height = Generator.find_in_tree(x, "int_height")[0]
            children_generators = Generator.from_item_list(Generator.find_in_tree(x, "item_list"), self.defs)
            if self.defs.has_type(ID.value):
                Generator.exception(ID.line, ID.column, ": Type identifier '" + ID.value + "' is already in use")
            if width != None and height != None:
                width = Integer(int(width))
                height = Integer(int(height))
            self.defs.add(TypeDef(ID.value, width, height, children_generators))

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