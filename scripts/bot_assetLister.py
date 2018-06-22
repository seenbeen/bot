import os
import fnmatch

def filterPyInit(filename):
    return (filename.endswith('.py') and not filename.startswith('__init__'))

matches = []
excludeDir = ['scripts','deprecated']
for root, dirnames, filenames in os.walk('../'):
    [dirnames.remove(d) for d in list(dirnames) if d in excludeDir]
    for filename in filter(filterPyInit, filenames):
        matches.append(os.path.join(root, filename))

searchLine = "AssetManager.instance().loadAsset("
assetLines = []
for match in matches:
    file = open(match, "r")
    for line in file:
        if searchLine in line:
            start = line.find("AssetManager.instance().loadAsset(\"") + len("AssetManager.instance().loadAsset(\"")
            end = line.rfind("\")")
            if (line[start:end][0] == "/" or line[start:end][0] == "\\"):
                assetLines.append(line[start+1:end])
            else:
                assetLines.append(line[start:end])
    file.close()

f = open("../assets/assetslist", "w+")
for asset in assetLines:
    f.write("%s\n"%asset)

f.close()
