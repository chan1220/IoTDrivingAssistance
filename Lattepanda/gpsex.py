from PyQt5 import QtCore, QtGui, QtWidgets
import time
import threading
import paho.mqtt.client as mqtt

class gpsex(QtCore.QThread):

	on_changed_gps     = QtCore.pyqtSignal(object)

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect("49.236.136.179", 1883, 60)

	def on_connect(self, client, userdata, rc, hehe):
		self.client.subscribe("SHK/GPS")

	def on_message(self, client, userdata, msg):
		print(msg.topic + " : " + msg.payload.decode('utf-8'))
		gps_str = msg.payload.decode('utf-8')
		gps_tuple = gps_str.split()
		gps_tuple = (float(gps_tuple[0]), float(gps_tuple[1]))
		self.on_changed_gps.emit(float())
	
	def stop(self):
		self.enabled = False

	def run(self):
		self.enabled = True
		self.client.loop_forever()
