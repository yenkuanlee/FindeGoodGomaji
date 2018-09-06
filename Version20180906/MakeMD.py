# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ScoreFlag = True

# Display
info = list()
info.append('name')
info.append('discount')
info.append('price')
info.append('orign_price')
info.append('sell_count')
info.append("google_rate")
info.append('gomaji_rate')
info.append('url')
info.append('open_time')
info.append('address')
info.append('description')
info.append('gomaji_rate_count')

f = open('result.json','r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    J = json.loads(line)
    for x in J:

        for y in info:
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
                print y+tmpp+str(J[x][y])+"\n"
            except Exception as e:
                pass
        try:
            if ScoreFlag:
                print "Sdict\n"
                for z in range(5,0,-1):
                    tmpp = ""
                    for i in range(10):
                        tmpp += "&nbsp;"
                    tmppp = ""
                    for i in range(30-len(str(z))):
                        tmppp += "&nbsp;"
                    print tmpp+str(z)+tmppp+str(J[x]['Sdict'][str(z)])+"\n"
        except Exception as e:
            print("@@@@@@@@@@@")
            print(str(e))
            pass
        print "\n==============================================================\n"
