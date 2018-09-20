import sys
Fnew = open(sys.argv[1],'r')
Fold = open(sys.argv[2],'r')
Gset = set()
OLD = ""
while True:
    line = Fold.readline()
    if not line:
        break
    if "gid=" in line:
        Gset.add(line.split("gid=")[1])

NEW = ""
flag = True
while True:
    line = Fnew.readline()
    if not line:
        break
    NEW += line
    if "gid=" in line:
        gid = line.split("gid=")[1]
        if gid in Gset:
            flag = False
    if "=====" in line:
        if flag:
            print(NEW)
        NEW = ""
        flag = True
