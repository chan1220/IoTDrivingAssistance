# coding: utf-8
 
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

from hehe import STT
from haha import TTS
import threading

from Weather import GetWeather

class Form(QtWidgets.QDialog):
	def __init__(self, parent=None):
		QtWidgets.QDialog.__init__(self, parent)
		self.ui = uic.loadUi("untitled.ui", self)
		self.ui.show()
		self.tts = TTS()

	@pyqtSlot()
	def slot_start(self):
		self.ui.stt.setText("--인식중--")
		self.ui.button_start.setEnabled(False)
		t = threading.Thread(target=self.gg)
		t.daemon = True
		t.start()

	@pyqtSlot()
	def slot_pause(self):
		print("정지?")


	def gg(self):
		self.gsp = STT()
		# 음성 인식 될때까지 대기 한다.
		stt = self.gsp.getText()
		# 만약 None이 반환되면
		if stt is None:
			return

		print(stt)
		self.ui.stt.setText(stt)

		if "꺼져" in stt:
			self.tts.play_tts("뭐라했냐 개새끼야아아?? 으아아앙??")
			self.ui.button_start.setEnabled(True)
			return

		if "안녕" in stt:
			self.tts.play_tts("반가워요??")
			self.ui.button_start.setEnabled(True)
			return

		if "날씨" in stt:
			wt = GetWeather()
			self.tts.play_tts(wt.getWeather())
			self.ui.button_start.setEnabled(True)
			return

		if ("유리" in stt) or ("일본 사람" in stt):
			self.tts.set_voice("yuri")
			self.tts.play_tts("저를 찾으셨나요?")
			self.ui.button_start.setEnabled(True)
			return
		else:
			self.tts.play_tts(stt)
			self.ui.button_start.setEnabled(True)
			return

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	w = Form()
	sys.exit(app.exec())
