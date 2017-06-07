# -*- coding: utf-8 -*-
import urllib2
def GetRate(name):
	resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+name+"&key=AIzaSyAVBk7wo_rABHQTo3JsZCWg0XG3s6zElLE&languages=zh")
	page = resp.read()
	if "\"rating\" : " in page:
		print page.split("\"rating\" : ")[1].split(",")[0]
		return
	print page

GetRate("5鄉地%20Cinque%20Terre")
