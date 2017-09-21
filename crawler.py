# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import urllib2
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
RateDict = dict()
fr = open('rate.index','r')
while True:
    line = fr.readline()
    if not line:
        break
    line = line.replace("\n","")
    tmp = line.split("\t")
    try:
        RateDict[tmp[0]] = tmp[1]
    except:
        pass
fr.close()

OldResult = dict()
fr = open('result.json','r')
while True:
    line = fr.readline()
    if not line:
        break
    OldResult = json.loads(line)
    break
fr.close()

def GetPid(name):
        try:
                resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+name+"&key=AIzaSyAVBk7wo_rABHQTo3JsZCWg0XG3s6zElLE&languages=zh")
                page = resp.read()
                if "\"place_id\" : " in page:
                        return page.split("\"place_id\" : ")[1].split(",")[0].replace("\"","")
        except:
                pass
        return "NO PID"
def GetRate(name):
        pid = GetPid(name)
        if pid == "NO PID":
                return "NO RATE"
        try:
                resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/details/json?place_id="+pid+"&key=AIzaSyAIt5DelcTj3pY_XyCetdR2MHAP6B-yXhg")
                page = resp.read()
                if "\"rating\" : " in page:
                        return page.split("\"rating\" : ")[1].split(",")[0]
        except:
                pass
        return "NO RATE"



def GetScore(page_source):
        Sdict = dict()
        if "<ul class=\"abox l\">" in page_source:
                tmp = page_source.split("<ul class=\"abox l\">")[1].split("</ul>")[0]
                tmpp = tmp.split("\n")
                for x in tmpp:
                        if ">非常滿意<" in x:
                                tmppp = x.split("</div></li>")[0].split(">")
                                Sdict['非常滿意'] = tmppp[len(tmppp)-1]
                        elif ">滿意<" in x:
                                tmppp = x.split("</div></li>")[0].split(">")
                                Sdict['滿意'] = tmppp[len(tmppp)-1]
                        elif ">普通<" in x:
                                tmppp = x.split("</div></li>")[0].split(">")
                                Sdict['普通'] = tmppp[len(tmppp)-1]
                        elif ">不滿意<" in x:
                                tmppp = x.split("</div></li>")[0].split(">")
                                Sdict['不滿意'] = tmppp[len(tmppp)-1]
                        elif ">非常不滿意<" in x:
                                tmppp = x.split("</div></li>")[0].split(">")
                                Sdict['非常不滿意'] = tmppp[len(tmppp)-1]
        return Sdict

def GetComment(info):
        response = urllib2.urlopen("http://www.gomaji.com/"+info+".html")
        page_source = response.read().replace("\n","").split("<div class=\"cbox\">")[1].split("<p class=\"clear\"></p>")[0]
        tmp = page_source.split("<div class=\"title\"><label>")
        for i in range(1,len(tmp),1):
                print "\t{"
                print "\tEmail : "+tmp[i].split("</label>")[0]
		print "\tRatingScore : "+tmp[i].split("rating_rating_s rating_s")[1].split("0 smile ")[0]
                print "\tContent : "+tmp[i].split("<div class=\"text l\">")[1].split("</div>")[0]
                print "\tDate : "+tmp[i].split("<div class=\"r\">")[1].split("</div>")[0]
                print "\t}"

Cdict = dict()
def Crawler(info):
        global RateDict
        global Cdict
	url = ""
	if "http" in info:
		url = info
	else:
		url = "http://www.gomaji.com/"+info+".html"

	response = urllib2.urlopen(url)
	page_source = response.read()

	Cflag = False
	if "此店家評價資料不足，累計10筆評價留言後才會顯示喔" not in page_source:
		#print "good good eat : "+info
		Cflag = True

	tmp = page_source.split("<script type=\"application/ld+json\">")[1].split("</script>")[0]
	Rdict = dict()
	tmpp = tmp.split("\n")
	for x in tmpp:
		if "\"name\"" in x:
			Rdict['name'] = x.split("\"")[3].split(" - GOMAJI")[0]
		elif "\"productID\"" in x:
			Rdict['productID'] = x.split("\"")[3]
		elif "\"image\"" in x:
			Rdict['image'] = x.split("\"")[3]
		elif "\"description\"" in x:
			Rdict['description'] = x.split("\"")[3]
		elif "\"url\"" in x:
			Rdict['url'] = x.split("\"")[3]
		elif "\"price\"" in x:
			Rdict['price'] = x.split("\"")[3]
	
	if "<p>地址：" in page_source:
		Rdict['address'] = page_source.split("<p>地址：")[1].split("\n")[0].split("\r")[0]
	if "<p>電話：" in page_source:
		Rdict['phone_number'] = page_source.split("<p>電話：")[1].split("</p>")[0]
	if "<p>營業時間：" in page_source:
		Rdict['open_time'] = page_source.split("<p>營業時間：")[1].split("</p>")[0]
        if "原價 <span><s>$" in page_source:
                Rdict['orign_price'] = page_source.split("原價 <span><s>$")[1].split("<")[0]

	Rdict['Sdict'] = GetScore(page_source)

        if int(Rdict['price']) > 300:return
        if float(Rdict['price']) / float(Rdict['orign_price']) > 0.8:
                return

        Rdict['discount'] = str(float(Rdict['price']) / float(Rdict['orign_price']))
        if Rdict['productID'] in RateDict:
            Rdict['rate'] = RateDict[Rdict['productID']]
        else:
            Rdict['rate'] = GetRate(Rdict['name'].replace(" ","%20"))
            RateDict[Rdict['productID']] = Rdict['rate']
            print "Call GetRate : "+Rdict['name']
            #Rdict['rate'] = "TESTTEST"

        Cdict[Rdict["productID"]] = Rdict

f = open(sys.argv[1],'r')
while True:
	line = f.readline()
	if not line : break
	line = line.replace("\n","")
	try:
		Crawler(line)
	except:
		print "error : "+line

Joutput = json.dumps(Cdict)
fw = open('result.json','w')
fw.write(Joutput)
fw.close()

index_update = open('rate.index','w')
for x in RateDict:
    index_update.write(x+"\t"+RateDict[x]+"\n")
index_update.close()



def send_email(recipient, subject, body):
    import smtplib
    user = ""
    pwd = ""
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print 'successfully sent the mail'
    except Exception,e:
        print "failed to send mail"
for x in Cdict:
    if x not in OldResult:
        print "new item : "+x
        send_email("yenkuanlee@gmail.com",Cdict[x]["name"],"[name]\t\t"+Cdict[x]["name"]+"\n\n[discount]\t\t"+Cdict[x]["discount"]+"\n\n[price]\t\t"+Cdict[x]["price"]+"\n\n[orign_price]\t\t"+Cdict[x]["orign_price"]+"\n\n[rate]\t\t"+Cdict[x]["rate"]+"\n\n[phone_number]\t\t"+Cdict[x]["phone_number"]+"\n\n[productID]\t\t"+Cdict[x]["productID"]+"\n\n[url]\t\t"+Cdict[x]["url"]+"\n\n[open_time]\t\t"+Cdict[x]["open_time"]+"\n\n[address]\t\t"+Cdict[x]["address"]+"\n\n[description]\t\t"+Cdict[x]["description"])
