# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Argument
ScoreFlag = True    # default = True
ScoreCondition = True  # default = True
AllowNoRate = True  # default = True
AllowNoAvgPrice = True # default = True
U_price = 400     # default = 400
U_avg_price = 400   # default = 400
U_discount = 0.8    # default = 0.7
B_rate = 3.5        # default = 3.5

# Display
info = list()
info.append('name')
info.append('discount')
info.append('price')
info.append('orign_price')
info.append('avg_price')
info.append('rate')
#info.append('phone_number')
#info.append('productID')
info.append('url')
#info.append('open_time')
info.append('address')
info.append('description')

f = open('result.json','r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    J = json.loads(line)
    for x in J:
        try:
            # filter by some condition
            if J[x]['rate']=="NO RATE":
                if AllowNoRate:
                    pass
                else:
                    continue
            elif float(J[x]['rate']) < B_rate:
                continue
            if int(J[x]['price']) > U_price:
                continue

            if not AllowNoAvgPrice:
                if "avg_price" not in J[x]:
                    continue

            try:
                if int(J[x]['avg_price']) > U_avg_price:
                    continue
            except:
                pass

            if float(J[x]['discount']) > U_discount:
                continue
        except:
            continue

        try:
            Score = J[x]["Sdict"].keys()
            for xx in Score:
                if xx == "非常滿意":
                    a = int(J[x]["Sdict"][xx])
                elif xx == "滿意":
                    b = int(J[x]["Sdict"][xx])
                elif xx == "普通":
                    c = int(J[x]["Sdict"][xx])
                elif xx == "不滿意":
                    d = int(J[x]["Sdict"][xx])
                elif xx == "非常不滿意":
                    e = int(J[x]["Sdict"][xx])
        
            SCFLAG = True
            if ScoreCondition:
                # ScoreCondition
                SClist = list()
                SClist.append( (a+b) > 10*(d+e) )
                SClist.append( (a+b+c+d+e) > 20 )
                for sc in SClist:
                    SCFLAG = SCFLAG and sc

            if not SCFLAG:
                continue
        except:
            pass

        for y in info:
            if y == "avg_price":
                if y not in J[x]:
                    continue
            try:
                tmpp = ""
                for i in range(30-len(y)):
                    tmpp += "&nbsp;"
                if y == "price":
                    tmpp += "&nbsp;&nbsp;&nbsp;"
                elif y == "rate":
                    tmpp += "&nbsp;&nbsp;&nbsp;&nbsp;"
                elif y == "url":
                    tmpp += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                elif y == "orign_price":
                    tmpp = tmpp[:len(tmpp)-6]
                elif y == "avg_price":
                    tmpp = tmpp[:len(tmpp)-6]
                print y+tmpp+J[x][y]+"\n"
            except:
                pass
        try:
            if ScoreFlag:
                print "Sdict\n"
                for z in J[x]['Sdict']:
                    tmpp = ""
                    for i in range(10):
                        tmpp += "&nbsp;"
                    tmppp = ""
                    for i in range(30-len(z)):
                        tmppp += "&nbsp;"
                    print tmpp+z+tmppp+J[x]['Sdict'][z]+"\n"
        except:
            pass
        print "\n==============================================================\n"
