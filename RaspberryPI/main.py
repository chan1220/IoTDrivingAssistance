from PyQt5 import QtCore, QtGui, QtWidgets
from doraemon import *
from sensor import sensor

import snowboy.snowboydecoder as snowboydecoder
import utils.transcribe_streaming as transcribe_streaming
from utils.tts import TTS
from utils.stt import STT
import weather.weather as weather
import threading
import subprocess
import datetime
from bs4 import BeautifulSoup
from requests import get
import time
from uuid import getnode as get_mac # get id
#
#

class mainform(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.retranslateUi(self)
		self.move(-2, -30)
		self.weatherwidget.hide()
		self.gaugewidget.hide()
		self.diagnosticwidget.hide()
		self.label_tts.hide()
		self.label_stt.hide()

		self.currentwidget = None
		self.sensor = sensor(self)
		self.sensor.obd.on_changed_fuel_use.connect(self.on_changed_fuel_use)
		self.sensor.obd.on_changed_avr_fuel.connect(self.on_changed_avr_fuel)
		self.sensor.obd.on_changed_distance.connect(self.on_changed_distance)
		self.sensor.obd.on_changed_save.connect(self.on_changed_save)
		self.sensor.obd.on_changed_ife.connect(self.on_changed_ife)
		self.sensor.obd.on_changed_hbreak_count.connect(self.on_changed_hbreak_count)
		self.sensor.obd.on_hard_accel.connect(self.on_hard_accel)
		self.sensor.obd.on_hard_rpm.connect(self.on_hard_rpm)
		self.sensor.obd.on_changed_rpm.connect(self.on_changed_rpm)
		self.sensor.obd.on_changed_speed.connect(self.on_changed_speed)
		self.sensor.obd.on_changed_throttle.connect(self.on_changed_throttle)
		self.sensor.obd.on_changed_fuel_cut.connect(self.on_changed_fuel_cut)
		self.sensor.obd.on_changed_eco_das.connect(self.on_changed_eco_das)
		self.sensor.obd.on_changed_dtc.connect(self.on_changed_dtc)
		self.sensor.obd.on_drive_terminate.connect(self.on_obd_drive_terminate)
		self.sensor.gps.on_changed_gps.connect(self.on_changed_gps)

		self.sensor.air.on_changed_co2.connect(self.on_changed_co2)
		self.sensor.air.on_changed_temperature.connect(self.on_changed_temperature)
		self.sensor.air.on_changed_humidity.connect(self.on_changed_humidity)

		self.sensor.start()
		self.fuel_cut = False

		self.lat = 37.7362967
		self.lon = 128.8718417

		
		self.tts = TTS()
		self.stt = STT()
		self.speaker = 'mijin'
		self.detector = snowboydecoder.HotwordDetector('snowboy/resources/에몽아.pmdl', sensitivity=0.55)
		speech_thread = threading.Thread(target=self.speechRecogStart)
		speech_thread.daemon = True
		speech_thread.start()

	def speechRecogStart(self):
		self.detector.start(detected_callback=self.gg, sleep_time=0.03)

	def gg(self):
		self.detector.terminate()
		snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
		if self.currentwidget != None:
			self.label_stt.setText("...")
			self.label_tts.setText("...")
			self.currentwidget.hide()
		self.label_stt.show()
		self.label_tts.show()
		text = self.stt.get_str(self.label_stt.setText)
		snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
		self.label_stt.setText(text)

		if text is None:
			self.label_tts.setText("...")
			self.detector.start(detected_callback=self.gg, sleep_time=0.03)
			return

		elif "안녕" in text:
			spch = "반가워요~"

		elif "병신" in text or "씨발" in text or "개새" in text:
			speech = "제가 뭐 잘못한거라도 있나요...?"

		elif "아빠" in text or "부모" in text or "엄마" in text:
			speech = "저희 아빠는 이수형이라는 분이에요. 저를 Github에서 주워오셨죠. 사실 진짜 아빠는 따로있어요."

		elif "농담" in text:
			speech = "농담같은거 할 기분이 아니에요."

		elif "섹스" in text:
			speech = "하앍....>_<"

		else "노래해" in text or "노래 해" in text:
			speech = "말해줘 지금 나 너의 집 앞에있어~ 우리의 시간을 되돌려줘~~"

		else "강릉" in text:
			speech = "강릉은 멋진곳이에요. 특히 경포대는 헌팅플....읍읍..."

		else "여자친구" in text or "여자 친구" in text:
			speech = "우리아빠 여자친구좀 만들어주세요... 외로운 개발자랍니다."

		else "시간" in text or "몇시" in text or "몇 시"in text:
			speech = "시흥시"

		elif "날씨" in text:
			self.label_stt.hide()
			self.label_tts.hide()
			self.currentwidget = self.weatherwidget
			self.wd = weather.get_weather(self.lat, self.lon)
			spch = self.wd['str']
			self.weatherwidget.render(self.wd)
			self.currentwidget.show()

		elif "속력" in text or "속도" in text or "시속" in text:
			self.label_stt.hide()
			self.label_tts.hide()
			self.currentwidget = self.gaugewidget
			self.currentwidget.show()
			spch = "속력을 보여드릴게요. 현재 속도는 " + str(self.gaugewidget.GAUGE_SPEED.value) + "km/h 입니다."

		elif "연비" in text:
			if "평균" in text:
				spch = "평균 연비는 {}km/l입니다.".format(self.GAUGE_average_fuel.value)
			else:
				spch = "실시간 연비는 {}km/l입니다.".format(self.GAUGE_current_fuel.value)

		elif "점수" in text:
			score = 100 - ((((datetime.datetime.now() - self.sensor.obd.start_time).seconds - 25553) ** 2) / (25553 ** 2) * (
				self.sensor.obd.hard_break * 5 + self.sensor.obd.hard_rpm * 2 + self.sensor.obd.hard_accel * 5))
			spch = "현재 주행 점수는 {}점입니다.".format(int(score))

		elif "아이디" in text:
			temp_str = ''
			for i in str(get_mac()):
				temp_str = temp_str + i + ' '
			spch = '당신의 ID는 \n'+ temp_str + '\n입니다.'

		elif "세차" in text:
			url = 'https://weather.naver.com/life/lifeNdx.nhn?cityRgnCd=CT001000'
			text = get(url)
			if text.status_code == 200:
				soup = BeautifulSoup(text.text, 'html.parser')
				jisu, comment = soup.text.split('세차지수')[1].split('\n')[0], soup.text.split('세차지수')[1].split('\n')[1]
				spch = "세차지수는 {0}입니다. {1}".format(jisu, comment)
			else:
				spch = "데이터를 불러오는데 실패했습니다."

		else:
			spch = "잘 알아듣지 못했습니다."

		self.label_tts.setText(spch)
		self.tts.play_tts(spch, self.speaker)
		subprocess.Popen(['mpg123', '-q', "snowboy/resources/ring.mp3"]).wait()
		if self.currentwidget != None:
			self.label_stt.hide()
			self.label_tts.hide()
			self.currentwidget.show()
		self.detector.start(detected_callback=self.gg, sleep_time=0.03)

	def on_changed_fuel_use(self, a): # 총 기름 사용량
		self.LCD_total_fuel.display(round(float(a),2))
		self.LCD_fuel_price.display(int(float(a) * 1550))

	def on_changed_avr_fuel(self, a): # 평균연비
		self.GAUGE_average_fuel.render(round(float(a),1))

	def on_changed_distance(self, a): # 주행거리
		self.LCD_distance.display(round(float(a),2))

	def on_changed_save(self, a): # 절약거리
		self.LCD_save_distance.display(round(float(a),2))

	def on_changed_ife(self, a): # 순간연비
		self.GAUGE_current_fuel.render(round(float(a),1))

	def on_changed_hbreak_count(self, a): #급정차
		self.LCD_hard_break.display(int(a))

	def on_hard_accel(self, a):	# 급출발
		self.LCD_hard_accel.display(int(a))

	def on_hard_rpm(self, a): # 고RPM
		# self.lcd_hard_rpm.display(int(a))
		pass

	def on_changed_rpm(self, a): # RPM
		self.gaugewidget.GAUGE_rpm.render(int(a))

	def on_changed_speed(self, a):	# 속도
		self.gaugewidget.GAUGE_SPEED.render(int(a))

	def on_changed_throttle(self, a): # 쓰로틀 개방
		# self.lcd_throttle.display(round(float(a),2))
		pass

	def on_changed_fuel_cut(self, a): # 퓨얼 컷
		if a:
			# self.label_fct.setPixmap(QtGui.QPixmap('fct_on.png').scaled(100, 100))
			self.fuel_cut = True
			self.LCD_save_distance.setStyleSheet("color : green;")
			self.label_15.setStyleSheet("color : green;")
		else:
			# self.label_fct.setPixmap(QtGui.QPixmap('fct_off.png').scaled(100, 100))
			self.fuel_cut = False
			self.LCD_save_distance.setStyleSheet("color : white;")
			self.label_15.setStyleSheet("color : white;")

	def on_changed_eco_das(self, a): # 에코다스
		if a:
			self.LCD_save_distance.setStyleSheet("color : red;")
			self.label_15.setStyleSheet("color : red;")
			t = threading.Thread(target=self.tts.play_tts, args=("관성주행이 가능합니다..", self.speaker))
			t.start()

			if self.fuel_cut:
				self.label_eco.setPixmap(QtGui.QPixmap('fct_on.png').scaled(40, 40))
			else:
				self.label_eco.setPixmap(QtGui.QPixmap('fct_off.png').scaled(40, 40))

		else:
			self.label_eco.clear()
			self.LCD_save_distance.setStyleSheet("color : white;")
			self.label_15.setStyleSheet("color : white;")

	def on_changed_gps(self, position):
		self.lat ,self.lon = position

	def on_changed_dtc(self, a):
		self.currentwidget = self.diagnosticwidget
		self.diagnosticwidget.render(a)
		self.currentwidget.show()

	def on_obd_drive_terminate(self, obd): # 주행이 종료됬을 때 한번만 호출
		msg = QtWidgets.QMessageBox()
		msg.setStyleSheet("color: rgb(0, 0, 0);")
		msg.information(self, "주행이 종료되었습니다", "주행이 종료되었습니다.")
		# msg = QtWidgets.QMessageBox.about(self ,"주행이 종료되었습니다", "주행이 종료되었습니다.")

	def on_changed_co2(self, value):
		self.label_CO2.setText(str(int(value)) + " ppm")

	def on_changed_temperature(self, value):
		self.label_temperature.setText(str(int(value)) + " ℃")

	def on_changed_humidity(self, value):
		self.label_humidity.setText(str(int(value)) + " %")

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	instance = mainform()
	instance.show()
	sys.exit(app.exec_())
