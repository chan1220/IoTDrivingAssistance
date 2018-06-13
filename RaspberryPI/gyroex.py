from PyQt5 import QtCore, QtGui, QtWidgets
import smbus
import math
import time


class gyroex(QtCore.QThread):

	on_changed_gyro = QtCore.pyqtSignal(object)

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.enabled = False
		self.power_mgmt_1 = 0x6b
		self.bus = smbus.SMBus(1)
		self.address = 0x68
		self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

	def read_word(self, adr):
		high = self.bus.read_byte_data(self.address, adr)
		low = self.bus.read_byte_data(self.address, adr + 1)
		val = (high << 8) + low
		return val

	def read_word_2c(self, adr):
		val = self.read_word(adr)
		if val >= 0x8000:
			return -((65535 - val) + 1)
		else:
			return val

	def dist(self, a, b):
		return math.sqrt((a * a) + (b * b))

	def get_x_rotation(self, x, y, z):
		radians = math.atan2(y, self.dist(x, z))
		return -math.degrees(radians)

	def stop(self):
		self.enabled = False

	def run(self):
		self.enabled = True
		
		while True and self.enabled:
			time.sleep(0.5)
			accel_xout_scaled = self.read_word_2c(0x3b) / 16384.0
			accel_yout_scaled = self.read_word_2c(0x3d) / 16384.0
			accel_zout_scaled = self.read_word_2c(0x3f) / 16384.0
				
			x_rotation = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
			self.on_changed_gyro.emit(x_rotation)

