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
        Welcome.resize(645, 530)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Welcome)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.create_file_button = QtWidgets.QPushButton(Welcome)
        self.create_file_button.setObjectName("create_file_button")
        self.verticalLayout_2.addWidget(self.create_file_button)
        self.open_file_button = QtWidgets.QPushButton(Welcome)
        self.open_file_button.setObjectName("open_file_button")
        self.verticalLayout_2.addWidget(self.open_file_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Welcome)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listView = QtWidgets.QListView(Welcome)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Welcome)
        self.open_file_button.clicked.connect(Welcome.on_open_file)
        self.create_file_button.clicked.connect(Welcome.on_create_file)
        QtCore.QMetaObject.connectSlotsByName(Welcome)

    def retranslateUi(self, Welcome):
        _translate = QtCore.QCoreApplication.translate
        Welcome.setWindowTitle(_translate("Welcome", "Form"))
        self.create_file_button.setText(_translate("Welcome", "CreateFile"))
        self.open_file_button.setText(_translate("Welcome", "OpenFile"))
        self.label.setText(_translate("Welcome", "Files hstory"))


