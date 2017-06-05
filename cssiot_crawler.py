# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def GetRate(name):
        try:
	    resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+name+"&key=AIzaSyAIt5DelcTj3pY_XyCetdR2MHAP6B-yXhg&languages=zh")
	    page = resp.read()
	    if "\"rating\" : " in page:
	        return page.split("\"rating\" : ")[1].split(",")[0]
	        return
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

def Crawler(info):
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
			#Rdict['rate'] = GetRate(Rdict['name'])
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
        Rdict['rate'] = GetRate(Rdict['name'].replace(" ","%20"))

	Sdict = GetScore(page_source)

        if "新北市" in Rdict['address'] : return
        if int(Rdict['price']) > 300:return
        if float(Rdict['price']) / float(Rdict['orign_price']) > 0.7:
                return

        try:
            if float(Rdict['rate']) < 4.0:
                return
        except:
            pass

	print "{"
	for x in Rdict:
		print x+" : "+Rdict[x]
        ###print "rate : "+GetRate(Rdict['name'].replace(" ","%20"))

	print "score : "
	for x in Sdict:
		print "\t"+x+" : "+Sdict[x]
	#if Cflag:
	#	print "comment : "
	#	GetComment(info)
	print "}"
print "["
f = open(sys.argv[1],'r')
while True:
	line = f.readline()
	if not line : break
	line = line.replace("\n","")
	try:
		Crawler(line)
	except:
		print "error : "+line
print "]"

###Crawler("Taiwan_p142363")
