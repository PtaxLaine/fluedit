# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/welcome.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Welcome(object):
    def setupUi(self, Welcome):
        Welcome.setObjectName("Welcome")
        Welcome.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Welcome)
        self.verticalLayout.setObjectName("verticalLayout")
        self.open_file_button = QtWidgets.QPushButton(Welcome)
        self.open_file_button.setObjectName("open_file_button")
        self.verticalLayout.addWidget(self.open_file_button)
        self.create_file_button = QtWidgets.QPushButton(Welcome)
        self.create_file_button.setObjectName("create_file_button")
        self.verticalLayout.addWidget(self.create_file_button)

        self.retranslateUi(Welcome)
        QtCore.QMetaObject.connectSlotsByName(Welcome)

    def retranslateUi(self, Welcome):
        _translate = QtCore.QCoreApplication.translate
        Welcome.setWindowTitle(_translate("Welcome", "Form"))
        self.open_file_button.setText(_translate("Welcome", "OpenFile"))
        self.create_file_button.setText(_translate("Welcome", "CreateFile"))


