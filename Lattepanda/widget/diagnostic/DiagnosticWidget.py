from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

class DiagnosticWidget(QWidget):
	def __init__(self, parent):
		super(DiagnosticWidget, self).__init__(parent)
		self.setObjectName("Form")
		self.resize(600, 600)
		self.setMaximumSize(QSize(600, 600))
		self.setStyleSheet("background-color: rgb(39, 41, 43);")
		self.gridLayout_2 = QGridLayout(self)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.gridLayout = QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.label_11 = QLabel(self)
		self.label_11.setText("")
		self.label_11.setObjectName("label_11")
		self.gridLayout.addWidget(self.label_11, 14, 2, 1, 2)
		self.label = QLabel(self)
		self.label.setStyleSheet("font: 11pt \"HY헤드라인M\";\n"
"color : rgb(24, 136, 255);\n"
"border : 1px solid rgb(24, 136, 255);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.15 rgba(235, 148, 61, 255), stop:0.78 rgba(0, 0, 0, 128), stop:1 rgba(0, 0, 0, 0));\n"
"")
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 2, 1, 1, 3)
		self.label_13 = QLabel(self)
		self.label_13.setStyleSheet("font: 13pt \"HY헤드라인M\";\n"
"color: rgb(0, 85, 255);")
		self.label_13.setAlignment(Qt.AlignCenter)
		self.label_13.setObjectName("label_13")
		self.gridLayout.addWidget(self.label_13, 5, 2, 1, 2)
		self.label_code = QLabel(self)
		self.label_code.setStyleSheet("font: 10pt \"HY헤드라인M\";\n"
"color: rgb(255, 0, 0);")
		self.label_code.setAlignment(Qt.AlignCenter)
		self.label_code.setObjectName("label_code")
		self.gridLayout.addWidget(self.label_code, 7, 1, 6, 1)
		self.line = QFrame(self)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		self.line.setObjectName("line")
		self.gridLayout.addWidget(self.line, 4, 1, 1, 3)
		self.label_12 = QLabel(self)
		self.label_12.setStyleSheet("font: 13pt \"HY헤드라인M\";\n"
"color: rgb(0, 85, 255);")
		self.label_12.setAlignment(Qt.AlignCenter)
		self.label_12.setObjectName("label_12")
		self.gridLayout.addWidget(self.label_12, 5, 1, 1, 1)
		self.label_description = QLabel(self)
		self.label_description.setStyleSheet("font: 10pt \"HY헤드라인M\";\n"
"color: rgb(0, 255, 0);")
		self.label_description.setAlignment(Qt.AlignCenter)
		self.label_description.setObjectName("label_description")
		self.gridLayout.addWidget(self.label_description, 7, 2, 6, 2)
		self.label_2 = QLabel(self)
		self.label_2.setStyleSheet("image: url(car_scan.png);")
		self.label_2.setText("")
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
		self.line_2 = QFrame(self)
		self.line_2.setFrameShape(QFrame.HLine)
		self.line_2.setFrameShadow(QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.gridLayout.addWidget(self.line_2, 13, 1, 1, 3)
		self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
		self.label.setText("   [차량 진단]")
		self.label_13.setText("[Description]")
		self.label_code.setText("발견된 고장 코드가 없습니다.")
		self.label_12.setText("[Error Code]")
		self.label_description.setText("차량이 정상입니다.")


	def render(self, error_list):
		if len(error_list) <= 0:
			return
		else:
			code = ""
			desc = ""
			for error in error_list:
				code = code + error[0] + '\n\n'
				desc = desc + error[1] + '\n\n'
			self.label_description.setText(desc)
			self.label_code.setText(code)				



