#Script to generate the Constants.py file

# all definitions must end with this suffix
definitionSuffix = "_definition"

definitions = []
attributes = []
enums = []
with open("../../global_grammar.lark") as grammar: # TODO use regex?
    while (line := grammar.readline()):
        line = line.strip()
        if (line.startswith("_") or len(line) == 0):
            continue

        identifierEndIndex = line.find(":")
        identifier = line[0:identifierEndIndex]

        # if the line is a definition
        if (identifier.endswith(definitionSuffix)):
            definitions.append((identifier[0:identifier.find(definitionSuffix)].upper(), identifier))
            currentEnum = ""

        # if the line is an identifier (TODO find a better option tan valid python identifier)
        elif (identifier.isidentifier() and identifier.islower()):
            attributes.append((identifier.upper(), identifier))

        # if the line is a terminal (i.e. enum) # TODO currently all enums values must be on 1 line
        elif (identifier.isidentifier() and identifier.isupper() and line.__contains__("|")):
            enums.append((identifier, line[identifierEndIndex+1:].replace("\"","").replace(" ", "").split("|")))

# TODO now loop over and make sure we don't have any enums that are marked as "%ignore"

# generate the Constants.py file
header = '''# AUTO-GENERATED FILE. DO NOT MODIFY DIRECTLY
# To regenerate run `python3 ConstantsBuilder.py` form this directory

from enum import Enum

def asList(enum):
    result = []
    for val in enum:
        result.append(val.value)
    return result
'''

extraConstants = '''class IMG_FORMATS(Enum):
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    SVG = "svg"
    
class DEFAULTS:
	COLOR = "#000"
'''

strDefs = "class DEFS (Enum):\n"

for d in definitions:
    strDefs += f"\t {d[0]} = \"{d[1]}\"\n"


strAttribs = "class ATTRIBS (Enum):\n"

for a in attributes:
    strAttribs += f"\t {a[0]} = \"{a[1]}\"\n"

strEnums = ""

for e in enums:
    strEnums += f"class {e[0]} (Enum):\n"
    for v in e[1]:
        strEnums += f"\t {v.upper()} = \"{v}\"\n"
    strEnums += "\n"


output = f'''
{header}
{extraConstants}
{strDefs}
{strAttribs}
{strEnums}
'''

f = open("Constants.py", "w")
f.write(output)
f.close()
