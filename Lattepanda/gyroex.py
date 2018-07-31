from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as mqtt
import time
import threading
from uuid import getnode as get_mac

class gyroex(QtCore.QThread):

	on_changed_gyro = QtCore.pyqtSignal(object)

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect("49.236.136.179", 1883, 60)

	def on_connect(self, client, userdata, rc, hehe):
		self.client.subscribe(str(get_mac()) + "/gyro")

	def on_message(self, client, userdata, msg):
		# print(msg.topic + " : " + msg.payload.decode('utf-8'))
		self.on_changed_gyro.emit(float(msg.payload.decode('utf-8')))
	
	def stop(self):
		self.enabled = False

	def run(self):
		self.enabled = True
		self.client.loop_forever()


if __name__ == "__main__":

	def hehe(r):
		print(r)

	gyro = gyroex()
	gyro.on_changed_gyro.connect(hehe) 
	gyro.start()
	while True:
		pass