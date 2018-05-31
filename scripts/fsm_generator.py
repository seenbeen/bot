import sys

# Script to generate FSM Templates, because this crap will
# drive anyone crazy writing

def usage():
    print "Usage: python %s <output_file_name> <className> <start_state> [state2] ... [staten]"%sys.argv[0]
    sys.exit(-1)

argc = len(sys.argv)

if argc <= 3:
    usage()

outputName = sys.argv[1]
className = sys.argv[2]
startState = sys.argv[3]
stateNames = [startState]+sys.argv[4:]

fopen = open(outputName,"w")

# import line
fopen.write("from bot_framework.bot_fsm import *\n")
fopen.write("\n")

# generate a class definition
fopen.write("class %s(BOTFSM):\n"%(className))

# throw in all our default state methods
for state in stateNames:
    fopen.write(" "*4 + "# %s\n"%(state))
    for meth in [["Init", []], ["TransitionFrom", ["fromState"]], ["TransitionTo", ["toState"]], ["Update", ["deltaTime"]], ["LateUpdate", []]]:
        fopen.write(" "*4 + "@staticmethod\n")
        fopen.write(" "*4 + "def __%s%s(%s):\n"%(state, meth[0], "self" + ", "*(len(meth[1]) > 0) + ", ".join(meth[1])))
        fopen.write(" "*8 + "pass\n")
        fopen.write("\n")
    fopen.write("\n")

# now for the init function that links everything
fopen.write(" "*4 + "def init(self):\n")
fopen.write(" "*8 + "states = [\n")
tempStates = []
for state in stateNames:
    tempState = ""
    tempState += (" "*12 + "BOTFSMState(self, \"%s\",\n"%(state))
    tempState += (" "*16 + "{\n")
    for meth in ["init", "transitionFrom", "transitionTo", "update", "lateUpdate"]:
        tempState += (" "*20 + "\"%s\" : self.__%s%s,\n"%(meth,state,meth[0].upper()+meth[1:]))
    tempState += (" "*16 + "})")
    tempStates.append(tempState)
fopen.write(",\n".join(tempStates)+"\n")
fopen.write(" "*12 + "]\n")
fopen.write(" "*8 + "initState = \"%s\"\n"%(startState))
fopen.write(" "*8 + "return [initState, states]\n")

# finally, close file
fopen.close()
