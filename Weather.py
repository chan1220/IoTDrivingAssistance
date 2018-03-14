import json
import urllib.request
import os
import sys
import pygame
import time
# 테스트용 Python Dictionary

class GetWeather:
	def getWeather(self):
		api_url = "http://apis.skplanetx.com/weather/current/minutely?appKey=7e828ecb-7f1a-36ec-b0ca-d199fc12a578&version=1&lat=37.34860159999999&lon=126.7271088" #위도/경도
		jsonString = urllib.request.urlopen(api_url).read().decode('utf8')

		# 문자열 출력
		#print(jsonString) # class str

		dict = json.loads(jsonString)
		#print(dict["weather"]["minutely"])

		type 	= dict["weather"]["minutely"][0]["precipitation"]["type"]
		sky 	= dict["weather"]["minutely"][0]["sky"]["name"]
		tc 		= dict["weather"]["minutely"][0]["temperature"]["tc"]
		tmax 	= dict["weather"]["minutely"][0]["temperature"]["tmax"]
		tmin 	= dict["weather"]["minutely"][0]["temperature"]["tmin"]
		humi 	= dict["weather"]["minutely"][0]["humidity"]
		time 	= dict["weather"]["minutely"][0]["timeObservation"]
		wdir 	= dict["weather"]["minutely"][0]["wind"]["wdir"]
		wspd 	= dict["weather"]["minutely"][0]["wind"]["wspd"]

		print("강수형태 : ",dict["weather"]["minutely"][0]["precipitation"]["type"])
		print("하늘 : ",dict["weather"]["minutely"][0]["sky"]["name"])
		print("온도 : ",dict["weather"]["minutely"][0]["temperature"]["tc"])
		print("최고온도 : ",dict["weather"]["minutely"][0]["temperature"]["tmax"])
		print("최저온도 : ",dict["weather"]["minutely"][0]["temperature"]["tmin"])
		print("상대습도 : ",dict["weather"]["minutely"][0]["humidity"])
		print("관측시간 : ",dict["weather"]["minutely"][0]["timeObservation"])
		print("풍향 : ",dict["weather"]["minutely"][0]["wind"]["wdir"])
		print("풍속 : ",dict["weather"]["minutely"][0]["wind"]["wspd"])


		str = time + "에 관측된 기상 정보를 알려드리겠습니다. 현재 하늘은 " + sky + "이고 현재온도는 " + tc + "도 입니다."
		return str

