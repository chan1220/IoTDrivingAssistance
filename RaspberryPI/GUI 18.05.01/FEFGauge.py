from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FEFGauge(QWidget):
    def __init__(self, parent):
        super(FEFGauge, self).__init__(parent)
        self.setGeometry(0, 0, 385, 70)

        self.value = 0.0
        self.label_name = self.set_label(10, 5, 40, 25, '연비')
        self.label_value = self.set_label(5, 30, 120, 70, str(self.value), True)
        self.label_unit = self.set_label(130, 45, 40, 25, 'Km/L')

    def set_label(self, x, y, width, height, text, value=False):
        font = QFont()
        font.setBold(True)
        label = QLabel(self)
        if value:
            font.setPixelSize(40)
            label.setAlignment(Qt.AlignRight)
        else:
            font.setPixelSize(15)
        label.setFont(font)
        label.setText(text)
        label.setStyleSheet('color: rgb(132, 132, 132)')
        label.setGeometry(x, y, width, height)
        return label

    def render(self, response):
        self.value = response
        self.update()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        self.label_value.setText(str(self.value))
        gauge_value = int(self.value)
        for i in range(gauge_value):
            if i > 29:
                continue
            if gauge_value < 5:
                painter.setPen(QPen(QColor(0xE33400), 4))
            elif 5 <= gauge_value < 15:
                painter.setPen(QPen(QColor(255, 255, 0), 4))
            else:
                painter.setPen(QPen(QColor(0, 255, 0), 4))
            painter.drawLine(180 + i * 6, 30, 180 + i * 6, 70)
        painter.end()
