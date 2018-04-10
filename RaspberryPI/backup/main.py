# ====== PyQt5 =======
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# ====== Widgets ======
import FEFGauge
# ====== Control ======
from sys import argv
from time import sleep


class QtForm(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('tjfgusrhks')
        self.setGeometry(0, 0, 800, 450)

        # =============== Widget Init =================
        self.gauge_fef = FEFGauge.FEFGauge(self, 174)

        # ============== Init Label ===================
        self.label_name_dis = self.set_name_label('주행거리')
        self.label_name_afef = self.set_name_label('평균연비')
        self.label_unit_dis = self.set_unit_label('Km')
        self.label_unit_afef = self.set_unit_label('Km/L')
        self.label_dis = self.set_value_label()
        self.label_afef = self.set_value_label()

        font = QFont()
        font.setBold(True)
        font.setPixelSize(40)
        font.setFamily('GyeonggiTitleM')
        self.label_name = QLabel(self)
        self.label_name.setFont(font)
        self.label_name.setText('설현관')
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet('color: rgb(20, 20, 20)')

        # ================= Widget Position ==============
        self.label_name.setGeometry(3, 3, 300, 84)
        self.gauge_fef.setGeometry(3, 183, 174, 174)
        self.label_name_dis.setGeometry(190, 180, 100, 40)
        self.label_name_afef.setGeometry(190, 270, 100, 40)
        self.label_unit_dis.setGeometry(290, 230, 100, 50)
        self.label_unit_afef.setGeometry(290, 320, 100, 50)
        self.label_dis.setGeometry(180, 205, 220, 50)
        self.label_afef.setGeometry(180, 295, 220, 50)

        self.label_dis.setText('0')

        # ================= Back Color ====================
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(0x323232))
        self.setPalette(palette)

        # ================== Worker ==========================
        self.worker = Worker()
        self.worker.change_fef.connect(self.gauge_fef.render)
        self.worker.change_afef.connect(self.label_afef.setText)
        self.worker.start()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(0x323232)
        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)
        brush = QBrush(QColor(0x6897BB))
        painter.setBrush(brush)
        painter.drawRect(QRect(0, 0, 400, 90))
        brush = QBrush(QColor(0x202020))
        painter.setBrush(brush)
        painter.drawRect(QRect(0, 90, 400, 90))
        painter.drawRect(QRect(0, 180, 180, 180))
        painter.drawRect(QRect(180, 180, 220, 90))
        painter.drawRect(QRect(180, 270, 220, 90))
        painter.drawRect(QRect(0, 360, 400, 90))
        painter.end()

    def set_name_label(self, text):
        font = QFont()
        font.setBold(True)
        font.setPixelSize(15)
        font.setFamily('GyeonggiTitleM')
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)
        label.setStyleSheet('color: white')
        return label

    def set_value_label(self):
        font = QFont()
        font.setBold(True)
        font.setPixelSize(40)
        font.setFamily('GyeonggiTitleM')
        label = QLabel(self)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('color: white')
        return label

    def set_unit_label(self, text):
        font = QFont()
        font.setBold(True)
        font.setPixelSize(15)
        font.setFamily('GyeonggiTitleM')
        label = QLabel(self)
        label.setText(text)
        label.setFont(font)
        label.setAlignment(Qt.AlignRight)
        label.setStyleSheet('color: white')
        return label


class Worker(QThread):
    # ======== signal init ============
    change_fef = pyqtSignal(float)
    change_afef = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True

        self.m_dis = 0

        self.m_cl = 0
        self.m_al = 0

    def __del__(self):
        self.wait()

    def set_tmp(self, r):
        self.change_fef.emit(round(r, 1))

    def set_ama(self, l):
        self.change_afef.emit(str(round(sum(l, 0.0) / len(l), 1)))

    def run(self):
        i = 0.0
        j = True
        li = list()
        while True:
            sleep(0.01)
            if j:
                i += 0.1
            else:
                i -= 0.1
            li.append(i)
            if int(i) is 35:
                j = False
            elif int(i + 0.5) is 0:
                j = True
            self.set_tmp(i)
            self.set_ama(li)


if __name__ == '__main__':
    app = QApplication(argv)
    form = QtForm()
    form.show()
    app.exec_()
