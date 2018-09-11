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

f = open('../result.json','r')
print("## 我的邀請碼 Q7ZLL , 歡迎輸入一起賺點數唷\n")
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    line = line.replace("~","-")
    J = json.loads(line)

    ### Kevin Filter
    RemoveList = list()
    BadPlace = ['蘆洲', '五股', '樹林', ]
    for x in J:
        r = J[x]['Sdict']
        good = r['5']
        bad = r['1']+r['2']+r['3']+r['4']
        if J[x]['sell_count']<100:
            RemoveList.append(x)
        elif bad==0:
            continue
        elif (float(good)/float(bad)) < 2:
            RemoveList.append(x)
        else:
            for y in BadPlace:
                if y in J[x]['address']:
                    RemoveList.append(x)
                    break
    for x in RemoveList:
        J.pop(x,None)

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
