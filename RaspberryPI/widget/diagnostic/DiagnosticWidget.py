from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widget.diagnostic.Diagnostic import Ui_Form

class DiagnosticWidget(QWidget, Ui_Form):
	def __init__(self, parent):
		QWidget.__init__(self, parent)
		self.setupUi(self)
		self.label_img.setPixmap(QPixmap("widget/diagnostic/good.png"))
		self.pushButton.clicked.connect(self.onClickLabel)

	def render(self, error_list):
		if len(error_list) <= 0:
			self.pushButton.hide()
			return
		else:
			self.label_img.setPixmap(QPixmap("widget/diagnostic/broken.png"))
			self.label_result.setStyleSheet("color: red")
			self.label_result.setText("진단 결과 {}개의 문제를 발견했습니다.".format(len(error_list)))
			self.error_list = error_list

	def onClickLabel(self):
		for error in self.error_list:
			msgbox = QMessageBox()
			msgbox.setStyleSheet("color: rgb(0, 0, 0);")
			msgbox.information(self, "고장코드", "({0}) {1}".format(error[0], error[1]))