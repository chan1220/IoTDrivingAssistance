from PyQt5 import QtCore, QtGui, QtWidgets
from widget.gauge.gauge import Ui_Form


class GaugeWidget(QtWidgets.QWidget, Ui_Form):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.retranslateUi(self)
