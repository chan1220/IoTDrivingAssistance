# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Diagnostic.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(385, 420)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.label_img = QtWidgets.QLabel(Form)
        self.label_img.setGeometry(QtCore.QRect(40, 90, 300, 188))
        self.label_img.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.label_img.setText("")
        self.label_img.setPixmap(QtGui.QPixmap("good.png"))
        self.label_img.setObjectName("label_img")
        self.label_result = QtWidgets.QLabel(Form)
        self.label_result.setGeometry(QtCore.QRect(0, 290, 385, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_result.setFont(font)
        self.label_result.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.label_result.setStyleSheet("color: rgb(0, 255, 0);")
        self.label_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_result.setObjectName("label_result")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(250, 360, 93, 28))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_result.setText(_translate("Form", "차량에 이상이 없습니다."))
        self.pushButton.setText(_translate("Form", "결과 확인"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

