import sys
import os

if sys.argv[1] == "--help":
    print("First cmdline argument can be a directory (relative to cd)"
          "and the other arguments can be file endings including the dot.")
    exit()

directory = '.' # Default directoy for os.listdir()
if sys.argv[1][0] != "." or sys.argv[1][0:3] == "../":
    directory = sys.argv[1]
    print("Search root directory:", directory)
    if directory[-1] != '/':
        directory += '/'

def GetLoc(fileName):
    with open(fileName, "r") as file:
        lines = sum(1 for line in file)
        print(fileName, "has", lines, "of code")
        return lines

argbegin = 1
if directory != '.':
    argbegin = 0
loc = 0
for root, dirs, files in os.walk(directory):
    for file in files:
        for arg in sys.argv[1:]:
            if file.endswith(arg):
                fullpath = os.path.join(root, file)
                loc += GetLoc(fullpath)

print("Total lines of code:", loc)
