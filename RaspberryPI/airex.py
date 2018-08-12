from PyQt5 import QtCore, QtGui, QtWidgets
import time
import threading
import paho.mqtt.client as mqtt
from uuid import getnode as get_mac

class airex(QtCore.QThread):

	on_changed_humidity     = QtCore.pyqtSignal(object)
	on_changed_temperature  = QtCore.pyqtSignal(object)
	on_changed_co2 		    = QtCore.pyqtSignal(object)

	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect("49.236.136.179", 1883, 60)

	def on_connect(self, client, userdata, rc, hehe):
		self.client.subscribe(str(get_mac()) + "/temperature")
		self.client.subscribe(str(get_mac()) + "/humidity")
		self.client.subscribe(str(get_mac()) + "/co2")

	def on_message(self, client, userdata, msg):
		print(msg.topic + " : " + msg.payload.decode('utf-8'))
		if msg.topic == str(get_mac()) + "/temperature":
			self.on_changed_temperature.emit(float(msg.payload.decode('utf-8')))

		if msg.topic == str(get_mac()) + "/humidity":
			self.on_changed_humidity.emit(float(msg.payload.decode('utf-8')))

		if msg.topic == str(get_mac()) + "/co2":
			self.on_changed_co2.emit(float(msg.payload.decode('utf-8')))


	def stop(self):
		self.enabled = False

	def run(self):
		self.enabled = True
		self.client.loop_forever()
