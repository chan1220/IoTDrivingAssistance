#-*- coding: utf-8 -*-

import json
import urllib.request
import requests

import weather.mise as mise
# import mise
# import pos
import weather.pos as pos

sky_dict = {'SKY_D01': "맑은 날씨", 'SKY_D02': '구름이 조금 있는 날씨', 'SKY_D03': '구름이 많은 날씨', 'SKY_D04': '흐린 날씨', 'SKY_D05': '비가 오는 날씨', 'SKY_D06': '눈이 오는 날씨', 'SKY_D07': '비 또는 눈이 오는 날씨'}
tomorrow_sky_dict = {'SKY_M01': "맑은 날씨", 'SKY_M02': '구름이 조금 있는 날씨', 'SKY_M03': '구름이 많은 날씨', 'SKY_M04': '흐린 날씨', 'SKY_M05': '비가 오는 날씨', 'SKY_M06': '눈이 오는 날씨', 'SKY_M07': '비 또는 눈이 오는 날씨'}

def get_weather_str(addr, temp, tmax, tmin, sky, dust, dust_str):
	weather_str = "{}의 현재 온도는 {} 도 이고, 오늘의 최고 기온은 {} 도, 최저 기온은 {} 도 이며, {}입니다. ".format(addr, round(float(temp),1), round(float(tmax),1), round(float(tmin),1), sky)
	weather_str = weather_str + "또한 미세먼지 농도는 {}마이크로그램 퍼 제곱미터 이고, 상태는 {}입니다.".format(dust, dust_str)
	return weather_str


def get_weather(lat, lon):

	current_weather = requests.get("https://api2.sktelecom.com/weather/current/hourly?version=1&lat={}&lon={}&appKey=fda2fe2c-3ad4-42fd-9162-4ad9ce9bf0e5".format(lat, lon))
	current_result = current_weather.json()
	
	temperature = current_result['weather']['hourly'][0]['temperature']['tc']

	summary_weather = requests.get("https://api2.sktelecom.com/weather/summary?version=1&lat={}&lon={}&appKey=fda2fe2c-3ad4-42fd-9162-4ad9ce9bf0e5".format(lat, lon))
	result = summary_weather.json()

	sky_code = result['weather']['summary'][0]['today']['sky']['code']
	sky_code_str = result['weather']['summary'][0]['today']['sky']['name']
	tmax = result['weather']['summary'][0]['today']['temperature']['tmax']
	tmin = result['weather']['summary'][0]['today']['temperature']['tmin']

	tomorrow_sky_code = result['weather']['summary'][0]['tomorrow']['sky']['code']
	tomorrow_sky_code_str = result['weather']['summary'][0]['tomorrow']['sky']['name']
	tomorrow_tmax = result['weather']['summary'][0]['tomorrow']['temperature']['tmax']
	tomorrow_tmin = result['weather']['summary'][0]['tomorrow']['temperature']['tmin']


	addr = pos.get_addr(lat, lon)
	dust, dust_str = mise.get_mise(addr[:2])

	tomorrow_info = {'sky_code': tomorrow_sky_code, 'sky_name': tomorrow_sky_code_str, 't_max': tomorrow_tmax,'t_min': tomorrow_tmin}

	info_dict = {'addr': addr, 't_temp': temperature, 't_max': tmax, 't_min': tmin, 'sky_code':sky_code, 'sky_name': sky_code_str, 'dust': dust, 'dust_str': dust_str, 'tomorrow': tomorrow_info, 'str': get_weather_str(addr, temperature, tmax, tmin, sky_dict[sky_code], dust, dust_str) }

	return info_dict

if __name__ == "__main__":
	print(get_weather(37,127))