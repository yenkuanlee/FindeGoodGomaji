#-*- coding: UTF-8 -*-
import sys
f = open(sys.argv[1],'r')
Tdict = dict()
Tlist = list()
condition = dict()

condition["rate"] = 3.5
condition["discount"] = 0.7
condition["price"] = 300
condition["address"] = "新北市"

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
            if float(Tdict["rate"]) >= condition["rate"] and float(Tdict["discount"]) <= condition["discount"] and int(Tdict["price"]) <= condition["price"] and condition["address"] not in Tdict["address"]:
                print "{"
                for x in Tlist:
                    print x
                print "}"
        except Exception,e: 
            #print str(e)
            pass
    Tlist.append(line)
    tmp = line.split(" : ")
    if tmp[0] == "rate":
        #print tmp[1]
        Tdict["rate"] = tmp[1]
    elif tmp[0] == "discount":
        Tdict["discount"] = tmp[1]
    elif tmp[0] == "price" :
        Tdict["price"] = tmp[1]
    elif tmp[0] == "address" :
        Tdict["address"] = tmp[1]
