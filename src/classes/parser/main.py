#!/usr/bin/python

import sys

def main():
    f = ""
    if len(sys.argv) == 1:
        f = input("Enter file name: ")
    elif len(sys.argv) == 2:
        f = sys.argv[1]
    else:
        print("Please only pass up to one argument (the file to parse) to this command.")
        exit()

    with open(f) as fileContents:
        print(fileContents.read())
        # TODO DO THE MAGIC

main()