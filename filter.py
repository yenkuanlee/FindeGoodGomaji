# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Argument
ScoreFlag = True
AllowNoRate = True
U_price = 200
U_discount = 0.7
B_rate = 4.0

# Display
info = list()
info.append('name')
info.append('discount')
info.append('price')
info.append('orign_price')
info.append('rate')
info.append('phone_number')
info.append('productID')
info.append('url')
info.append('open_time')
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
            if float(J[x]['discount']) > U_discount:
                continue
        except:
            continue
        for y in info:
            print y+"\t\t"+J[x][y]
        try:
            if ScoreFlag:
                print "Sdict"
                for z in J[x]['Sdict']:
                    print "\t\t"+z+"\t"+J[x]['Sdict'][z]
        except:
            pass
        print "\n==============================================================\n"
