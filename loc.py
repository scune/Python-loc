import sys
import os

if sys.argv[1] == "--help":
    print("First cmdline argument can be a directory path,\n"
          "the other arguments can be file endings including the '.'\n"
          "or folder names that should be ignored using '-i' as a prefix.")
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
        print(fileName, "has", lines, "lines of code")
        return lines

argbegin = 1
if directory != '.':
    argbegin = 0

ignoreFolders = []
fileEndings = []
for i in range(argbegin, len(sys.argv)):
    if i > 0 and sys.argv[i - 1] == "-i":
        if sys.argv[i][-1] != "/":
            sys.argv[i] += '/'
        ignoreFolders.append(sys.argv[i])
    else:
        fileEndings.append(sys.argv[i])

loc = 0
for root, dirs, files in os.walk(directory):
    for file in files:
        fullpath = os.path.join(root, file)
        dirname =  os.path.join(fullpath, file)

        ignore = False
        for ignoreFolderName in ignoreFolders:
            if dirname.find(ignoreFolderName) != -1:
                ignore = True
                break;
        if ignore:
            continue

        for fileEnding in fileEndings:
            if file.endswith(fileEnding):
                loc += GetLoc(fullpath)

print("Total lines of code:", loc)
