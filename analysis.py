import sys
f = open(sys.argv[1],'r')
Tdict = dict()
Tlist = list()
condition = dict()

condition["rate"] = 4.5
condition["discount"] = 0.6
condition["price"] = 200

while True:
    line = f.readline()
    if not line:break
    line = line.replace("\n","")
    if line == "{": # Start
        Tdict = dict() # initial
        Tlist = list()
        continue
    elif line == "}": # End
        try:
            if float(Tdict["rate"]) >= condition["rate"] and float(Tdict["discount"]) <= condition["discount"] and int(Tdict["price"]) <= condition["price"]:
                print "{"
                for x in Tlist:
                    print x
                print "}"
        except:
            pass
    Tlist.append(line)
    tmp = line.split(" : ")
    if tmp[0] == "rate":
        Tdict["rate"] = tmp[1]
    elif tmp[0] == "discount":
        Tdict["discount"] = tmp[1]
    elif tmp[0] == "price" :
        Tdict["price"] = tmp[1]
    elif tmp[0] == "address" :
        Tdict["address"] = tmp[1]
