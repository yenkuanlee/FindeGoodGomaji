import sys
f = open(sys.argv[1],"r")
while True:
    line = f.readline()
    if not line:break
    if "Taipei_" not in line:continue
    print line,
