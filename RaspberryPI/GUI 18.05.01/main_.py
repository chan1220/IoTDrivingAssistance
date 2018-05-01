# ====== PyQt5 =======
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# ====== Widgets ======
import FEFGauge
import GaugeWindow
# ====== Control ======
from sys import argv
from time import sleep


class QtForm(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('GUI')
        self.resize(800, 450)

        # =============== Widget Init =================
        """ LEFT LCD """
        self.gauge_fef = FEFGauge.FEFGauge(self)

        """ RIGHT LCD """
        self.gauge_window = GaugeWindow.GaugeWindow(self)

        # ================= Widget Position ==============
        self.gauge_fef.setGeometry(15, 70, 385, 70)
        self.gauge_window.setGeometry(405, 40, 385, 410)

        # ============== Init Label ===================
        self.label_car_info = self.set_inform_label(25, 28, 200, 30, 'ROLLS-ROYCE\nPhantom EWB (2018)')
        self.label_usr_info = self.set_inform_label(320, 35, 50, 15, '설현관', True)
        self.label_fpr_name = self.set_label(20, 170, 100, 25, '사용유류비')
        self.label_fpr = self.set_price_label(10, 205, 180, 50, '0')
        self.label_fpr_unit = self.set_label(200, 220, 30, 25, '원')
        self.label_fsp_name = self.set_label(20, 315, 100, 25, '절약유류비')
        self.label_fsp = self.set_price_label(10, 350, 180, 50, '0', True)
        self.label_fsp_unit = self.set_label(200, 365, 30, 25, '원')
        self.label_dis_name = self.set_label(235, 155, 70, 25, '주행거리')
        self.label_dis = self.set_label(250, 185, 100, 40, '0.00', True)
        self.label_dis_unit = self.set_label(360, 190, 30, 25, 'Km')
        self.label_fam_name = self.set_label(235, 225, 80, 25, '소모유류량')
        self.label_fam = self.set_label(250, 255, 100, 40, '0.00', True)
        self.label_fam_unit = self.set_label(360, 260, 30, 25, 'L')
        self.label_sdi_name = self.set_label(235, 300, 70, 25, '절약거리')
        self.label_sdi = self.set_label(250, 330, 100, 40, '0.00', True)
        self.label_sdi_unit = self.set_label(360, 335, 30, 25, 'Km')
        self.label_sfa_name = self.set_label(235, 370, 70, 25, '절약유류량')
        self.label_sfa = self.set_label(250, 400, 100, 40, '0.00', True)
        self.label_sfa_unit = self.set_label(360, 405, 30, 25, 'L')

        # ================== Worker ==========================
        self.worker = Worker()
        self.worker.change_fef.connect(self.gauge_fef.render)
        self.worker.change_fpr.connect(self.label_fpr.setText)
        self.worker.change_fsp.connect(self.change_fsp)
        self.worker.change_dis.connect(self.label_dis.setText)
        self.worker.change_fam.connect(self.label_fam.setText)
        self.worker.change_sdi.connect(self.label_sdi.setText)
        self.worker.change_sfa.connect(self.label_sfa.setText)
        self.worker.change_rpm.connect(self.gauge_window.render_rpm)
        self.worker.change_spd.connect(self.gauge_window.render_spd)
        self.worker.change_bspd.connect(self.gauge_window.render_bspd)
        self.worker.change_bstp.connect(self.gauge_window.render_bstp)
        self.worker.start()

    def set_label(self, x, y, width, height, text, value=False):
        font = QFont()
        font.setBold(True)
        label = QLabel(self)
        if value:
            font.setPixelSize(25)
            label.setAlignment(Qt.AlignRight)
        else:
            font.setPixelSize(15)
        label.setFont(font)
        label.setText(text)
        label.setGeometry(x, y, width, height)
        label.setStyleSheet('color: rgb(245, 247, 249)')
        return label

    def set_inform_label(self, x, y, width, height, text, name=False):
        font = QFont()
        font.setBold(True)
        label = QLabel(self)
        font.setPixelSize(15)
        label.setFont(font)
        label.setText(text)
        if name:
            label.setAlignment(Qt.AlignRight)
        label.setStyleSheet('color: rgb(132, 132, 132)')
        label.setGeometry(x, y, width, height)
        return label

    def set_price_label(self, x, y, width, height, text, echo=False):
        font = QFont()
        font.setBold(True)
        font.setPixelSize(40)
        label = QLabel(self)
        if echo:
            label.setStyleSheet('color: rgb(245, 247, 249)')
        else:
            label.setStyleSheet('color: rgb(225, 60, 96)')
        label.setFont(font)
        label.setText(text)
        label.setAlignment(Qt.AlignRight)
        label.setGeometry(x, y, width, height)
        return label

    def change_fsp(self, value, sw):
        if sw:
            self.label_fsp.setStyleSheet('color: rgb(60, 225, 96)')
        else:
            self.label_fsp.setStyleSheet('color: rgb(245, 247, 249)')
        self.label_fsp.setText(value)

    def paintEvent(self, *args, **kwargs):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, QImage('img/bg.jpg'))
        painter.setBrush(QBrush(QColor(0x27292B)))
        painter.drawRoundedRect(QRect(10, 10, 385, 430), 15, 15)
        painter.drawRoundedRect(QRect(405, 10, 385, 430), 15, 15)
        painter.setBrush(QBrush(QColor(0xF2F2F2)))
        painter.drawRoundedRect(QRect(15, 15, 375, 135), 10, 10)
        painter.drawPolygon(QPoint(415, 25), QPoint(432, 15), QPoint(432, 35))
        painter.drawPolygon(QPoint(780, 25), QPoint(763, 15), QPoint(763, 35))
        painter.setPen(QPen(QColor(0xDBDBDB), 2))
        painter.drawLine(20, 70, 385, 70)
        painter.setPen(QPen(QColor(55, 57, 59), 4))
        painter.drawLine(15, 295, 390, 295)
        painter.setPen(QPen(QColor(55, 57, 59), 2))
        painter.drawLines(QLine(230, 152, 230, 439),
                          QLine(230, 222, 390, 222),
                          QLine(230, 367, 390, 367))
        painter.end()


class Worker(QThread):
    # ======== signal init ============
    change_fef = pyqtSignal(float)
    change_fpr = pyqtSignal(str)
    change_fsp = pyqtSignal(str, bool)
    change_dis = pyqtSignal(str)
    change_fam = pyqtSignal(str)
    change_sdi = pyqtSignal(str)
    change_sfa = pyqtSignal(str)
    change_rpm = pyqtSignal(int)
    change_spd = pyqtSignal(int)
    change_bspd = pyqtSignal(int)
    change_bstp = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True

    def __del__(self):
        self.wait()

    def set_fef(self, r):
        self.change_fef.emit(round(r, 1))

    def set_fpr(self, r):
        self.change_fpr.emit(format(int(round(r, 0)), ','))

    def set_fsp(self, r, s):
        self.change_fsp.emit(format(int(round(r, 0)), ','), s)

    def set_dis(self, r):
        self.change_dis.emit('{0:.2f}'.format(round(r, 2)))

    def set_fam(self, r):
        self.change_fam.emit('{0:.2f}'.format(round(r, 2)))

    def set_sdi(self, r):
        self.change_sdi.emit('{0:.2f}'.format(round(r, 2)))

    def set_sfa(self, r):
        self.change_sfa.emit('{0:.2f}'.format(round(r, 2)))

    def set_rpm(self, r):
        self.change_rpm.emit(int(round(r, 0)))

    def set_spd(self, r):
        self.change_spd.emit(int(round(r, 0)))

    def set_bspd(self, r):
        self.change_bspd.emit(int(round(r, 0)))

    def set_bstp(self, r):
        self.change_bstp.emit(int(round(r, 0)))

    def run(self):
        i = 0.00
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
            self.set_fef(i)
            self.set_fpr(i * 5000)
            self.set_fsp(i * 3000, j)
            self.set_dis(i/7)
            self.set_fam(i/3)
            self.set_sdi(i/21)
            self.set_sfa(i/44)
            self.set_rpm(i * 100)
            self.set_spd(i * 3)
            self.set_bspd(i)
            self.set_bstp(i)


if __name__ == '__main__':
    app = QApplication(argv)
    form = QtForm()
    form.show()
    exit(app.exec_())
