#-*- coding: utf-8 -*-
import sys
import urllib.request
import json
from urllib import parse


def get_mise(city):
	convert_dust_level = {u'1':u'좋음',u'2':u'보통',u'3':u'나쁨',u'4':u'매우나쁨'}
	url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=pbGF2mxEK2HNq6Xyl4qh3B9kq%2BSV%2FVq8LK3xetlrsNVTsQWhuTAtvxwPx6wc1pkWVHeZLuOF4nw5AYxnDyP2sQ%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&sidoName={}&ver=1.3&_returnType=json".format(parse.quote(city))
   
	jsonString = urllib.request.urlopen(url).read().decode('utf8')
	data = json.loads(jsonString)

	return (data["list"][1]["pm10Value"], convert_dust_level[data["list"][1]["pm10Grade"]])

	