import sys
import os

def Usage():
    print("Usage:\n"
          "The current directory path for the search can only be specified by the first command.\n"
          "Other arguments can be file endings while including the '.' and\n"
          "folder names that should be ignored using \"-i\" as a prefix command\n"
          "Preconfigured groups can be specified using the \"-g\" prefix command\n"
          "Current groups are \"c/c++\" and \"glsl\".")
    exit()

if sys.argv[1] == "--help":
    Usage()

directory = '.' # Default directoy for os.listdir()
if sys.argv[1][0] != "." or sys.argv[1][0:3] == "../":
    directory = sys.argv[1]
    if directory[-1] != '/':
        directory += '/'

    if directory != '.' and (not os.path.isdir(directory) or (os.listdir(directory)) == 0):
        print(directory, "doesn't exist or is empty!")
        exit()

    print("Search root directory:", directory[0:-1])

def PrintFileName(filePath, lines):
    filePath.co # TODO
    print("\t" * )
    print(filePath, "has", lines, "lines of code")

def GetLoc(filePath):
    with open(filePath, "r") as file:
        lines = sum(1 for line in file)
        filePath = filePath.removeprefix(directory)
        PrintFileName(filePath, lines)
        return lines

argbegin = 1
if directory != '.':
    argbegin = 0

def GetGroupFileEndings(groupName):
    if groupName == "c/c++":
        return [".cpp", ".hpp", ".c", ".h"]
    elif groupName == "glsl":
        return [".glsl",
                ".vert", ".frag",
                ".comp",
                ".rgen", ".rchit", ".rmiss", ".rcall", ".rahit"
                ".mesh", ".task"]
    else:
        print("No group with name", "\"" + groupName + "\"!");
        return []

ignoreFolders = []
fileEndings = []
ignoreFilePrefixes = ["."]
for i in range(argbegin, len(sys.argv)):
    if i > 0 and sys.argv[i - 1] == "-i":
        if sys.argv[i][-1] != '/':
            sys.argv[i] += '/'
        if sys.argv[i][0] != '/':
            sys.argv[i] = '/' + sys.argv[i];
        ignoreFolders.append(sys.argv[i])
    elif i > 0 and sys.argv[i - 1] == "-g":
        fileEndings.extend(GetGroupFileEndings(sys.argv[i]))
    else:
        fileEndings.append(sys.argv[i])

loc = 0
parsedFileCount = 0
for root, dirs, files in os.walk(directory):
    for file in files:
        fullpath = directory + os.path.join(root, file)

        if not file.endswith(tuple(fileEndings)):
            continue

        bIgnore = False
        for ignoreFolder in ignoreFolders:
            if fullpath.find(ignoreFolder) != -1:
                bIgnore = True
                break

        if bIgnore or file.startswith(tuple(ignoreFilePrefixes)):
            continue
        
        loc += GetLoc(fullpath)
        parsedFileCount += 1

if parsedFileCount == 0:
    print("No files found!")
    Usage()
elif parsedFileCount > 1:
    print("Total lines of code:", loc)