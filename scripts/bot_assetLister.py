'''
Limitations of the parser:

Only takes strings inbetween the load call, variables inside the brackets will NOT work(ex: load(class.NAME)
The argument is also not evaluated, load("foo" + "bar") will also not work

There cannot be a ") on the right of the load call for whatever reason.
load("foo.bar").foo("bar") will not work
'''
import sys, os
import fnmatch

os.chdir(os.path.dirname(sys.argv[0])+"/..")

def filterPyInit(filename):
    return (filename.endswith('.py') and not filename.startswith('__init__'))

def usage():
    print "Usage: python %s <output_file_name> <dir_to_search> <dir_to_exclude> <dir_to_exclude> ..."%sys.argv[0]
    sys.exit(-1)

argc = len(sys.argv)
if argc <= 1:
    usage()
    
excludeDir = []
if argc >= 3:
    for i in range(argc-3):
        excludeDir.append(sys.argv[i+3])

matches = []

dirPrefix = sys.argv[2]
if dirPrefix == ".":
    dirPrefix = ""
    
for root, dirnames, filenames in os.walk(dirPrefix):
    [dirnames.remove(d) for d in list(dirnames) if d in excludeDir]
    for filename in filter(filterPyInit, filenames):
        matches.append(os.path.join(root, filename))

searchLine = "AssetManager.instance().loadAsset("
assetLines = set()
for match in matches:
    file = open(match, "r")
    for line in file:
        if searchLine in line:
            start = line.find("AssetManager.instance().loadAsset(\"") + len("AssetManager.instance().loadAsset(\"")
            end = line.rfind("\")")
            if (line[start:end][0] == "/" or line[start:end][0] == "\\"):
                assetLines.add((line[start+1:end]))
            else:
                assetLines.add((line[start:end]))
    file.close()

f = open(sys.argv[1]+".botal", "w+")
for asset in assetLines:
    f.write("%s\n"%asset)

f.close()
