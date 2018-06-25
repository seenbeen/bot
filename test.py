import sys
import traceback

if len(sys.argv) == 1:
    print "Usage: %s <path-to-test1.py> <path-to-test2.py> ... <path-to-testn.py>"%(sys.argv[0])
    exit(0)

testNames = map(lambda x: ".".join(x.split(".")[0].split("/")), sys.argv[1:])

# get rid of __init__.py...
testNames = filter(lambda x: x.split(".")[-1] != "__init__", testNames)

# sadly couldn't find a better way to do this ;_;
exec("".join(map(lambda test: "import " + test + ";", testNames)))

# run and report our results
failures = []
for test in testNames:
    try:
        print "Running %s..."%(test)
        eval(test+".run()")
    except Exception as e:
        failures.append([test, sys.exc_info()])

# skip a line to make output cleaner
print ""

if failures:
    print "Testing Failed :<\n"
    print "The following tests failed:\n"
    for fail in failures:
        print fail[0]
        print "------------Stack Trace------------"
        traceback.print_exception(*fail[1])
        del fail[1]
        print "------------------------------------------------\n"
else:
    print "All tests passed! :DD"
        
