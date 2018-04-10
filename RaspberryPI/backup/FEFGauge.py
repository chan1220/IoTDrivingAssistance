from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from util import map_value


class FEFGauge(QWidget):
    def __init__(self, parent, size):
        super(FEFGauge, self).__init__(parent)
        self.xlen = self.ylen = size - 4
        self.setGeometry(0, 0, size, size)
        self.FONT_SIZE = size / 6
        self.font = QFont()
        self.font.setPixelSize(self.FONT_SIZE)
        self.font.setBold(True)
        self.font.setFamily('Arial Black')
        self.board_img = QImage('board.png').scaled(self.xlen, self.ylen)
        self.arrow_img = QImage('arrow.png').scaled(self.xlen, self.ylen)
        self.value = 0

    def render(self, response):
        self.value = response
        self.update()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawImage(QPoint(0, 0), self.board_img)
        self.draw_needle(painter)
        self.draw_value(painter)
        painter.end()

    def draw_value(self, painter):
        painter.save()
        color = QColor(0xFFFFFF)
        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setFont(self.font)
        r_height = self.xlen
        r = QRect(0, self.height() - (r_height * 0.95), self.width(), r_height)
        painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.value))
        painter.restore()

    def draw_needle(self, painter):
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        angle = map_value(self.value, 0, 30, 0, 310)
        angle = min(angle, 310)
        painter.rotate(angle)
        painter.drawImage(QPoint(-self.xlen/2, -self.ylen/2), self.arrow_img)
        painter.restore()
