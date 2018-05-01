from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import NeedleGauge


class GaugeWindow(QWidget):
    def __init__(self, parent):
        super(GaugeWindow, self).__init__(parent)
        self.setGeometry(0, 0, 385, 350)

        self.gauge_rpm = NeedleGauge.NeedleGauge(self, True)
        self.gauge_rpm.setGeometry(110, 0, 165, 165)
        self.gauge_spd = NeedleGauge.NeedleGauge(self)
        self.gauge_spd.setGeometry(60, 150, 265, 265)

        self.label_bspd = self.set_label(25, 20, 60, 25, '급가속')
        self.label_bstp = self.set_label(300, 20, 60, 25, '급정차')

        self.bspd_cnt = QLCDNumber(self)
        self.bspd_cnt.display(0)
        self.bspd_cnt.setGeometry(25, 50, 60, 60)
        self.bstp_cnt = QLCDNumber(self)
        self.bstp_cnt.display(0)
        self.bstp_cnt.setGeometry(300, 50, 60, 60)

    def set_label(self, x, y, width, height, text):
        font = QFont()
        font.setBold(True)
        font.setPixelSize(15)
        label = QLabel(self)
        label.setFont(font)
        label.setText(text)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(x, y, width, height)
        label.setStyleSheet('color: rgb(245, 247, 249)')
        return label

    def render_rpm(self, response):
        self.gauge_rpm.render(response)

    def render_spd(self, response):
        self.gauge_spd.render(response)

    def render_bspd(self, response):
        self.bspd_cnt.display(response)

    def render_bstp(self, response):
        self.bstp_cnt.display(response)
