from obdex import *
from gpsex import *

class sensor():
	def __init__(self, parent=None):
		self.obd = obdex(parent)
		self.obd.on_updated.connect(self.on_obd_updated)
		
		self.gps = gpsex(parent)
		self.gps.on_changed_gps.connect(self.on_changed_gps)

	def start(self):
		self.obd.start()
		self.gps.start()

	def stop(self):
		self.obd.stop()
		self.gps.stop()

	def on_obd_updated(self, obd):
		print('fuel use : ' + str(obd.fuel_use))
		# DB에다가 여러가지 정보들 넣기

	def on_changed_gps(self, position):
		print(position)
		# DB에다가 position 넣기