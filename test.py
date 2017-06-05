# -*- coding: utf-8 -*-
import urllib2
def GetRate(name):
	resp = urllib2.urlopen("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+name+"&key=AIzaSyAIt5DelcTj3pY_XyCetdR2MHAP6B-yXhg&languages=zh")
	page = resp.read()
	if "\"rating\" : " in page:
		print page.split("\"rating\" : ")[1].split(",")[0]
		return
	print "NO RATE"

GetRate("5鄉地%20Cinque%20Terre")
