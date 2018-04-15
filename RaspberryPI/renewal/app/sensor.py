from obdex import *
from gpsex import *
from db_requester import db_requester

class sensor():
	def __init__(self, parent=None):
		self.obd = obdex(parent)
		self.obd.on_updated.connect(self.on_obd_updated)
		self.obd.on_drive_terminate.connect(self.on_obd_drive_terminate)

		self.gps = gpsex(parent)
		self.gps.on_changed_gps.connect(self.on_changed_gps)

		self.db = db_requester('http://localhost:5000')

	def start(self):
		self.obd.start()
		self.gps.start()

	def stop(self):
		self.obd.stop()
		self.gps.stop()

	def _get_car_id(self): # 차량 id 얻기
		with open('/proc/cpuinfo', 'r') as f:
			for line in f:
				if line[0:6] == 'Serial':
					return str(line[17:26])

	def on_obd_updated(self, obd):
		print('id : Kalos') 
		print('속력 : ' + str(obd.speed))
		print('순간연비 : ' + str(obd.ife))
		# (차량id, 시간, 속력, 순간연비)

	def on_changed_gps(self, position):
		lat, lon = position
		self.db.request('update/gps', {'id': self._get_car_id(), 'lat': lat, 'lon': lon})
		# (차량id, 시간, 위도, 경도)

	def on_obd_drive_terminate(self, obd):
		# 주행이 종료되었을 때 기록
		# (차량id, 시작시간, 거리, 평균연비, 평균속도, 고RPM횟수, 급정차횟수, 급가속횟수, 주행점수, 주행거리, 종료시간)
		pass
