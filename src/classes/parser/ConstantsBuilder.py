#Script to generate the Constants.py file

import re

# all definitions must end with this suffix
definitionSuffix = "_definition"

# enums to exclude (write in all caps)
excludedEnums = ["HEX_COLOR"]

definitions = []
attributes = []
enums = []
ignoredEnums = []
ignoredEnums.extend(excludedEnums)
with open("../../global_grammar.lark") as grammar: 
    prevLineWasEnum = False
    while (line := grammar.readline()):
        line = line.strip()
        if (len(line) == 0 or line[0] == "_" or line[0:2] in ("//", "/*", "*/")):
            continue
        elif line[0:7] == "%ignore":
            ignoredEnums.append(line[8:])
            continue

        identifierEndIndex = line.find(":")
        if (identifierEndIndex != -1):

            identifier = line[0:identifierEndIndex]

            # if the line is a definition
            if (identifier.endswith(definitionSuffix)):
                definitions.append((identifier[0:identifier.find(definitionSuffix)].upper(), identifier))
                prevLineWasEnum = False

            # if the line is a terminal (i.e. enum)
            elif (re.search("[A-Z0-9]+[A-Z0-9_]*",identifier) is not None):
                enums.append((identifier, line[identifierEndIndex+1:].replace("\"","").replace(" ", "").split("|")))
                prevLineWasEnum = True

            # if the line is an identifier
            elif (re.search("(\?)?[a-z0-9]+[a-zA-Z0-9_]*",identifier) is not None):
                if (identifier[0] == "?"):
                    attributes.append((identifier[1:].upper(), identifier[1:]))
                    prevLineWasEnum = False
                else:
                    attributes.append((identifier.upper(), identifier))
                    prevLineWasEnum = False

        elif line.startswith("|") and prevLineWasEnum:
            enums[-1][1].extend(line.replace("\"","").replace(" ", "").split("|"))
            prevLineWasEnum = True


# remove ignored enums from the list
enums = list(filter(lambda x : x[0] not in ignoredEnums, enums))


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
	FILL_COLOR = "#000"
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
        if (len(v) == 0): # TODO find a way such that we can't get empty values
            continue
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
