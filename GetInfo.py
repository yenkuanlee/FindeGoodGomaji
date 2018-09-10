# -*- coding: UTF-8 -*-
import json
import urllib2
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
api_key = sys.argv[1]
Cdict = dict()
Fdict = dict()
f = open('filter.conf')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    line = line.replace(" ","")
    line = line.split("#")[0]
    tmp = line.split("=")
    try:
        Fdict[tmp[0]] = tmp[1]
    except:
        pass

RateDict = dict()
fr = open('rate.index','r')
while True:
    line = fr.readline()
    if not line:
        break
    line = line.replace("\n","")
    tmp = line.split("\t")
    try:
        RateDict[tmp[0]] = (tmp[1],float(tmp[2])) # rate, time
    except:
        pass
fr.close()

TaipeiFoodUrl = "https://www.gomaji.com/ch/7?sort=0&city=1&dist_group="
Ulist = list()
for i in range(16):
    Ulist.append(TaipeiFoodUrl+str(i+1))

def GetPid(name):
    try:
        resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+name+"&key="+api_key+"&languages=zh")
        page = resp.read()
        if "\"place_id\" : " in page:
            return page.split("\"place_id\" : ")[1].split(",")[0].replace("\"","")
    except:
        pass
    return "NO PID"
def GetGoogleRate(name):
    pid = GetPid(name)
    if pid == "NO PID":
        return "NO RATE"
    try:
        resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/details/json?place_id="+pid+"&key="+api_key)
        page = resp.read()
        if "\"rating\" : " in page:
            return page.split("\"rating\" : ")[1].split(",")[0]
    except:
        pass
    return "NO RATE"

def GetProductRate(gid):
    Rdict = dict()
    try:
        Rdict['status'] = 'SUCCESS'
        url = "https://ccc.gomaji.com/oneweb/product_rating_info?cat_id=0&ch_id=7&group_id="+gid
        response = urllib2.urlopen(url)
        Joutput = json.loads(response.read())
        rate = Joutput['data']['ratings']
        Rdict['rating_total_count'] = rate['rating_total_count']
        Rdict['avg_score'] = rate['avg_score']
        Rdict['score_cat_list'] = rate['score_cat_list']
        return Rdict
    except Exception as e:
        return {"status": "ERROR", "log": str(e)}

def GetProductInfo(url):
    Rdict = dict()
    try:
        Rdict['status'] = 'SUCCESS'
        response = urllib2.urlopen(url)
        result = response.read()
        try:
            description = result.split(" <meta name=\"description\" content=\"")[1].split("\">")[0]
        except:
            description = "NULL"
        tmp = result.split("<div class=\"store mb-3\">")[1].split("</div>")[0]
        try:
            address = tmp.split("地址：")[1].split("</p>")[0]
        except:
            address = "NULL"
        try:
            phone_number= tmp.split("電話：")[1].split("</p>")[0]
        except:
            phone_number = "NULL"
        try:
            open_time = tmp.split("營業時間：")[1].split("</p>")[0]
        except:
            open_time = "NULL"
        Rdict['description'] = description
        Rdict['address'] = address
        Rdict['phone_number'] = phone_number
        Rdict['open_time'] = open_time
        return Rdict
    except Exception as e:
        return {"status": "ERROR", "log": str(e)}


def GetPageInfo(url):
    global Cdict
    Rlist = list()
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        return {"status": "ERROR", "log": str(e)}
    page_source = response.read().replace("\n","")
    tmp = page_source.split("product-item border")
    for i in range(1,len(tmp)-1,1):
        Idict = dict()
        # Get 1-Info
        name = tmp[i].split("ellipsis\">")[1].split("<")[0]
        price = int(tmp[i].split("<div class=\"current\">")[1].split("$")[1].split("<")[0])
        orign_price = int(tmp[i].split("<div class=\"original line-through\">")[1].split("$")[1].split("<")[0])
        #discount = "%.2f" % (float(price)/float(orign_price))
        discount = float(price)/float(orign_price)
        url = "https://www.gomaji.com"+tmp[i].split("<a href=\"")[1].split("\"")[0]
        sell_count = tmp[i].split("t-orange t-085 pt-2")[1].split("<")[0]
        try:
            sell_count = int(re.search(r'\d+', sell_count).group())
        except:
            sell_count = 0
        # 1-Filter
        if price > int(Fdict['U_price']) :
            continue
        elif discount > float(Fdict['U_discount']):
            continue
        Idict['name'] = name
        Idict['price'] = price
        Idict['orign_price'] = orign_price
        Idict['discount'] = "%.2f" % discount
        Idict['url'] = url
        Idict['sell_count'] = sell_count

        # Get Rate-Info
        try:
            gid = url.split("gid=")[1]
        except:
            continue
        Prate = GetProductRate(gid)
        # Rate-Filter
        if Prate['status'] == "ERROR":
            continue
        elif Prate['avg_score'] < float(Fdict['L_gomaji_rate']):
            continue
        try:
            Idict['gomaji_rate'] = Prate['avg_score']
            Idict['gomaji_rate_list'] = Prate['score_cat_list']
            Idict['gomaji_rate_count'] = Prate['rating_total_count']
            Sdict = dict()
            for x in Idict['gomaji_rate_list']:
                Sdict[x['score']] = x['count']
            Idict['Sdict'] = Sdict
        except:
            Idict['gomaji_rate'] = "NULL"
            Idict['gomaji_rate_list'] = "NULL"
            Idict['gomaji_rate_count'] = "NULL"

        # Get 2-Info
        Pinfo = GetProductInfo(url)
        for p in Pinfo:
            Idict[p] = Pinfo[p]

        # Get Google Rate
        Ntime = time.time()
        if gid in RateDict:
            if (Ntime-RateDict[gid][1]) >= (86400*7):
                Idict['google_rate'] = GetGoogleRate(name)
                RateDict[gid] = (Idict['google_rate'],Ntime)
            else:
                Idict['google_rate'] = RateDict[gid][0]
        else:
            Idict['google_rate'] = GetGoogleRate(name)
            RateDict[gid] = (Idict['google_rate'],Ntime)
        if Idict['google_rate']=='NO RATE':
            pass
        elif float(Idict['google_rate']) < float(Fdict['L_google_rate']):
            continue
        Cdict[gid] = Idict
        Rlist.append(Idict)
    return Rlist

for i in range(16):
    GetPageInfo(Ulist[i])
fw = open('result.json','w')
fw.write(json.dumps(Cdict))
fw.close()

# Update Rate Index
fw = open('rate.index','w')
for pid in RateDict:
    fw.write(pid+"\t"+str(RateDict[pid][0])+"\t"+str(RateDict[pid][1])+"\n")
fw.close()
