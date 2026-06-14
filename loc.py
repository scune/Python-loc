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

directory = '.' # Default directory for os.listdir()
if sys.argv[1][0] != "." or sys.argv[1][0:3] == "../":
    directory = sys.argv[1]
    if directory[-1] != '/':
        directory += '/'

    if directory != '.' and (not os.path.isdir(directory) or (os.listdir(directory)) == 0):
        print(directory, "doesn't exist or is empty!")
        exit()

def GetLoc(filePath, filePrintData, depthOff):
    with open(filePath, "r") as file:
        lines = sum(1 for line in file)
        off = filePath.find("/") + 1
        depth = filePath.count("/", off) + 1 - depthOff
        filePrintData.append([filePath[off:], lines, depth])
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

filePrintData = []
loc = 0
parsedFileCount = 0
depthOff = max(0, directory.count("/") - 2)
for root, dirs, files in os.walk(directory):
    for file in files:
        fullpath = os.path.join(root, file)

        if not file.endswith(tuple(fileEndings)):
            continue

        bIgnore = False
        for ignoreFolder in ignoreFolders:
            if fullpath.find(ignoreFolder) != -1:
                bIgnore = True
                break

        if bIgnore or file.startswith(tuple(ignoreFilePrefixes)):
            continue
        
        loc += GetLoc(fullpath, filePrintData, depthOff)
        parsedFileCount += 1

T_RIGHT = "\u251c"     # ├
T_DOWN = "\u252c"      # ┬
BOTTOM_LEFT = "\u2514" # └
SOLID_LINE = "\u2500"  # ─

# Print file names with associated lines
# TODO: Folder line when depth decreases
prevDepth = 1
lineCache = set()
for i in range(len(filePrintData)):
    filePath, lines, depth = filePrintData[i]

    pipeChar = BOTTOM_LEFT
    pipeChar2 = SOLID_LINE
    nextDepth = 0
    if i + 1 < len(filePrintData):
        nextFilePath, nextLines, nextDepth = filePrintData[i + 1]
        if nextDepth >= depth:
            pipeChar = T_RIGHT
            pipeChar2 = T_DOWN
        
        if nextDepth > depth:
            higher_depth = False
            for j in range(i+2, len(filePrintData)):
                j_depth = filePrintData[j][2]
                if j_depth < nextDepth:
                    break
                if j_depth == nextDepth and higher_depth:
                    lineCache.add(depth)
                    break
                if j_depth > nextDepth:
                    higher_depth = True

    line0 = str()
    line1 = str()

    fileNameOff = filePath.rfind("/") + 1
    if prevDepth != depth: # Print new folder
        folderNameOff = filePath.rfind("/", 0, fileNameOff - 2) + 1

        line0 = " " * (4 * (depth - 1) - 2) + BOTTOM_LEFT + SOLID_LINE + filePath[folderNameOff:fileNameOff]

        line1 = " " * 4 * (depth - 1) + BOTTOM_LEFT + SOLID_LINE + pipeChar2 + SOLID_LINE + filePath[fileNameOff:] + " has " + str(lines) +  " lines of code"

        prevDepth = depth
    else:
        line0 = " " * (4 * depth - 2) + pipeChar + SOLID_LINE + filePath[fileNameOff:] + " has " + str(lines) +  " lines of code"

    for d in lineCache:
        d_idx = 4 * d - 2

        if line0[d_idx] == " ":
            line0 = line0[:d_idx] + "\u2502" + line0[d_idx + 1:]
        elif line0[d_idx] == BOTTOM_LEFT:
            line0 = line0[:d_idx] + T_RIGHT + line0[d_idx + 1:]

        if len(line1) > d_idx and line1[d_idx] == " ":
            line1 = line1[:d_idx] + "\u2502" + line1[d_idx + 1:]

    print(line0)
    if len(line1) > 0:
        print(line1)
    
    if nextDepth < depth and (nextDepth-1) in lineCache:
        lineCache.remove(nextDepth-1)

if parsedFileCount == 0:
    print("No files found!")
    Usage()
elif parsedFileCount > 1:
    print("Total lines of code:", loc)