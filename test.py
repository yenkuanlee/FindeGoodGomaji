# -*- coding: utf-8 -*-
import urllib2
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


print GetRate("lksajfa")		
#print GetRate("5鄉地%20Cinque%20Terre")
