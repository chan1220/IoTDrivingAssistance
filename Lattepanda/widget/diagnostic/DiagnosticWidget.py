from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

class DiagnosticWidget(QWidget):
	def __init__(self, parent):
		super(DiagnosticWidget, self).__init__(parent)
		self.path = os.getcwd() + "/widget/diagnostic/"
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setObjectName("verticalLayout")
		self.widget_3 = QWidget(self)
		self.widget_3.setObjectName("widget_3")
		self.gridLayout = QGridLayout(self.widget_3)
		self.gridLayout.setObjectName("gridLayout")
		self.line_2 = QFrame(self.widget_3)
		self.line_2.setFrameShape(QFrame.VLine)
		self.line_2.setFrameShadow(QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.gridLayout.addWidget(self.line_2, 4, 7, 1, 1, Qt.AlignBottom)
		self.line_4 = QFrame(self.widget_3)
		self.line_4.setFrameShape(QFrame.VLine)
		self.line_4.setFrameShadow(QFrame.Sunken)
		self.line_4.setObjectName("line_4")
		self.gridLayout.addWidget(self.line_4, 6, 7, 1, 1, Qt.AlignBottom)
		self.line_3 = QFrame(self.widget_3)
		self.line_3.setFrameShape(QFrame.VLine)
		self.line_3.setFrameShadow(QFrame.Sunken)
		self.line_3.setObjectName("line_3")
		self.gridLayout.addWidget(self.line_3, 5, 7, 1, 1, Qt.AlignBottom)
		self.line_21 = QFrame(self.widget_3)
		self.line_21.setFrameShape(QFrame.HLine)
		self.line_21.setFrameShadow(QFrame.Sunken)
		self.line_21.setObjectName("line_21")
		self.gridLayout.addWidget(self.line_21, 1, 2, 1, 5)
		self.line_22 = QFrame(self.widget_3)
		self.line_22.setFrameShape(QFrame.HLine)
		self.line_22.setFrameShadow(QFrame.Sunken)
		self.line_22.setObjectName("line_22")
		self.gridLayout.addWidget(self.line_22, 3, 2, 1, 5)
		self.label_13 = QLabel(self.widget_3)
		self.label_13.setStyleSheet("font: 11pt \"HY헤드라인M\";\n"
"color: rgb(0, 85, 255);\n"
"\n"
"")
		self.label_13.setAlignment(Qt.AlignCenter)
		self.label_13.setObjectName("label_13")
		self.gridLayout.addWidget(self.label_13, 2, 4, 1, 3)
		self.label_description = QLabel(self.widget_3)
		self.label_description.setStyleSheet("font: 10pt \"HY헤드라인M\";\n"
"color: rgb(0, 255, 0);\n"
"")
		self.label_description.setAlignment(Qt.AlignCenter)
		self.label_description.setObjectName("label_description")
		self.gridLayout.addWidget(self.label_description, 4, 4, 5, 3)
		self.line_16 = QFrame(self.widget_3)
		self.line_16.setStyleSheet("background: rgba(255,255,255,255);\n"
"color : rgba(255,255,255,255);")
		self.line_16.setFrameShape(QFrame.VLine)
		self.line_16.setFrameShadow(QFrame.Sunken)
		self.line_16.setObjectName("line_16")
		self.gridLayout.addWidget(self.line_16, 7, 7, 1, 1, Qt.AlignBottom)
		self.line_24 = QFrame(self.widget_3)
		self.line_24.setFrameShape(QFrame.VLine)
		self.line_24.setFrameShadow(QFrame.Sunken)
		self.line_24.setObjectName("line_24")
		self.gridLayout.addWidget(self.line_24, 4, 3, 5, 1)
		self.line_23 = QFrame(self.widget_3)
		self.line_23.setFrameShape(QFrame.VLine)
		self.line_23.setFrameShadow(QFrame.Sunken)
		self.line_23.setObjectName("line_23")
		self.gridLayout.addWidget(self.line_23, 2, 3, 1, 1)
		self.line_17 = QFrame(self.widget_3)
		self.line_17.setStyleSheet("background: rgba(255,255,255,255);\n"
"color : rgba(255,255,255,255);")
		self.line_17.setFrameShape(QFrame.VLine)
		self.line_17.setFrameShadow(QFrame.Sunken)
		self.line_17.setObjectName("line_17")
		self.gridLayout.addWidget(self.line_17, 8, 7, 1, 1, Qt.AlignBottom)
		self.label_12 = QLabel(self.widget_3)
		self.label_12.setStyleSheet("font: 11pt \"HY헤드라인M\";\n"
"color: rgb(0, 85, 255);\n"
"\n"
"\n"
"\n"
"")
		self.label_12.setAlignment(Qt.AlignCenter)
		self.label_12.setObjectName("label_12")
		self.gridLayout.addWidget(self.label_12, 2, 2, 1, 1)
		self.label_code = QLabel(self.widget_3)
		self.label_code.setStyleSheet("font: 10pt \"HY헤드라인M\";\n"
"color: rgb(255, 0, 0);\n"
"")
		self.label_code.setAlignment(Qt.AlignCenter)
		self.label_code.setObjectName("label_code")
		self.gridLayout.addWidget(self.label_code, 4, 2, 5, 1)
		self.line_11 = QFrame(self.widget_3)
		self.line_11.setMinimumSize(QSize(0, 3))
		self.line_11.setStyleSheet("background: rgba(255,255,255,255);\n"
"color : rgba(255,255,255,255);")
		self.line_11.setFrameShape(QFrame.HLine)
		self.line_11.setFrameShadow(QFrame.Sunken)
		self.line_11.setObjectName("line_11")
		self.gridLayout.addWidget(self.line_11, 10, 5, 1, 1, Qt.AlignLeft)
		self.line_8 = QFrame(self.widget_3)
		self.line_8.setFrameShape(QFrame.VLine)
		self.line_8.setFrameShadow(QFrame.Sunken)
		self.line_8.setObjectName("line_8")
		self.gridLayout.addWidget(self.line_8, 10, 0, 1, 1)
		self.line_18 = QFrame(self.widget_3)
		self.line_18.setFrameShape(QFrame.VLine)
		self.line_18.setFrameShadow(QFrame.Sunken)
		self.line_18.setObjectName("line_18")
		self.gridLayout.addWidget(self.line_18, 10, 7, 1, 1)
		self.widget = QWidget(self.widget_3)
		self.widget.setStyleSheet("QWidget#widget{\n"
"    background: rgba(255,255,255,255);\n"
"    border-radius: 15px;\n"
"    border : 1px solid white;\n"
"}")
		self.widget.setObjectName("widget")
		self.gridLayout_2 = QGridLayout(self.widget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.label_6 = QLabel(self.widget)
		font = QFont()
		font.setFamily("HY헤드라인M")
		font.setPointSize(14)
		self.label_6.setFont(font)
		self.label_6.setStyleSheet("color: rgb(168, 168, 168);\n"
"")
		self.label_6.setAlignment(Qt.AlignCenter)
		self.label_6.setObjectName("label_6")
		self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 2)
		self.label_5 = QLabel(self.widget)
		self.label_5.setStyleSheet("image: url({}.png);".format(self.path + 'obdscan'))
		self.label_5.setText("")
		self.label_5.setObjectName("label_5")
		self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.widget, 0, 2, 1, 5)
		self.verticalLayout.addWidget(self.widget_3)
		self.label_5.setBuddy(self.label_5)
		self.setWindowTitle("self")
		self.label_13.setText("[ Description ]")
		self.label_description.setText("차량이 정상입니다.")
		self.label_12.setText("[ Error Code ]")
		self.label_code.setText("차량이 정상입니다.")
		self.label_6.setText("[ 차량 진단 결과 ]")


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
