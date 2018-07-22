import sys
import os
'''
Limitations of the parser:

Only takes strings inbetween the load call, variables inside the brackets will NOT work(ex: load(class.NAME)
The argument is also not evaluated, load("foo" + "bar") will also not work

There cannot be a ") on the right of the load call for whatever reason.
load("foo.bar").foo("bar") will not work
'''

def usage():
    print "Usage: python %s <output_file_name> <dir_to_search> <dir_to_exclude> <dir_to_exclude> ..."%sys.argv[0]
    sys.exit(-1)

argc = len(sys.argv)
if argc <= 2:
    usage()
 
f = open(sys.argv[1]+".botal", "w+")
   
os.chdir(os.path.dirname(sys.argv[2]))
  
def filterPyInit(filename):
    return (filename.endswith('.py') and not filename.startswith('__init__'))

excludeDir = []

if argc >= 3:
    for i in range(argc-3):
        excludeDir.append(sys.argv[i+3])

matches = []
for root, dirnames, filenames in os.walk("."):
    [dirnames.remove(d) for d in list(dirnames) if d in excludeDir]
    for filename in filter(filterPyInit, filenames):
        matches.append(os.path.join(root, filename))

searchLinePrefix = ".loadAsset(\""
searchLinePostfix = "\")"
assetLines = set()
for match in matches:
    pyfile = open(match, "r")
    for line in pyfile:
        if searchLinePrefix in line:
            start = line.find(searchLinePrefix) + len(searchLinePrefix)
            end = line.rfind(searchLinePostfix)
            assetLines.add(line[start:end])
    pyfile.close()

for asset in assetLines:
    f.write("%s\n"%asset)

f.close()

