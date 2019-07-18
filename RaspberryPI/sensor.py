from obdex import *
from gpsex import *
from airex import *
from db_requester import db_requester
import datetime
from uuid import getnode as get_mac

class sensor():
	def __init__(self, parent=None):
		self.obd = obdex(parent)
		self.obd.on_updated.connect(self.on_obd_updated)
		self.obd.on_drive_terminate.connect(self.on_obd_drive_terminate)
		self.obd.on_changed_dtc.connect(self.on_changed_dtc)

		self.gps = gpsex(parent)
		self.gps.on_changed_gps.connect(self.on_changed_gps)

		self.air = airex(parent)
		# self.ari.on_changed_humidity.connect(self.on_changed_humidity)
		# self.ari.on_changed_temperature.connect(self.on_changed_temperature)
		# self.ari.on_changed_co2.connect(self.on_changed_co2)

		self.db = db_requester('http://15.164.149.11:5000') # 클라우드(웹서버) 주소
		self.id = self._get_car_id()
		print('당신의 차량 id : ',self.id)
	def start(self):
		self.obd.start()
		self.gps.start()
		self.air.start()

	def stop(self):
		self.obd.stop()
		self.gps.stop()
		self.air.stop()

	def _get_car_id(self): # 차량 id 얻기
		return(str(get_mac()))

	def on_obd_updated(self, obd): # 매 초당 주행 정보
		self.db.request('update/drive', {'id': self.id, 'fuel_efi': obd.ife, 'speed': obd.speed})

	def on_changed_gps(self, position): # GPS 정보
		lat, lon = position
		self.db.request('update/gps', {'id': self.id, 'lat': lat, 'lon': lon})

	def on_obd_drive_terminate(self, obd): # 주행이 종료됬을 때 한번만 호출
		self.obd.stop() # GPS 정지
		print("sexsex")
		avr_fuel_efi = obd.distance / obd.fuel_use
		lapse_sec = (datetime.datetime.now() - obd.start_time).seconds
		avr_speed = obd.distance / (lapse_sec / 3600)
		score = 100 - (((lapse_sec - 25553) ** 2) / (25553 ** 2) * (obd.hard_break * 5 + obd.hard_rpm * 2 + obd.hard_accel * 5))
		if score < 0:
			score = 0
		self.db.request('update/record', {'id': self.id, 'start_time': obd.start_time.strftime("%Y-%m-%d %H:%M:%S"), 'fuel_efi': avr_fuel_efi, 'avr_speed': avr_speed, 'hard_rpm': obd.hard_rpm, 'hard_break': obd.hard_break, 'hard_accel': obd.hard_accel, 'score': score, 'distance': obd.distance})
		print('zazi')

	def on_changed_dtc(self, code_list):
		for code in code_list:
			self.db.request('update/code', {'id': self.id, 'code': code[0], 'description': code[1]})

	def on_changed_co2(self, value):
		pass

	def on_changed_temperature(self, value):
		pass

	def on_changed_co2(self, value):
		pass

